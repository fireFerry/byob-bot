from discord.ext import commands
import discord
import json
import datetime
import asyncio
import chat_exporter
import io
import os
from datetime import datetime, timedelta
import cogs.utils as utils


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # blacklist command

    @commands.command()
    @commands.has_role('Support Team')
    async def blacklist(self, ctx, member: discord.Member):
        await utils.togglerole(member, discord.utils.get(ctx.guild.roles, name="Ticket Blacklist"), ctx)

    # contributor command
    @commands.command()
    @commands.has_role('Support Team')
    async def contributor(self, ctx, member: discord.Member):
        await utils.togglerole(member, discord.utils.get(ctx.guild.roles, name="Contributor"), ctx)

    # toggleautorole command to toggle automatically giving the Member role after membership screening

    @commands.command()
    @commands.has_role('Support Team')
    async def toggleautorole(self, ctx):
        autorolestatus, autoroles = await utils.autorole_status(ctx.guild.id)
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/autorole.json")
        if autorolestatus == 'on':
            autoroles[str(ctx.guild.id)] = 'off'
            status = "Disabled"
        else:
            autoroles[str(ctx.guild.id)] = 'on'
            status = "Enabled"
        with open(path, 'w') as f:
            json.dump(autoroles, f, indent=4)
        await utils.send_embed("Autorole toggled",
                               f"{status} autorole for this server.",
                               ctx,
                               False)

    # userinfo command that displays information about the user.

    @commands.command(aliases=['ui'])
    @commands.has_role('Support Team')
    async def userinfo(self, ctx, member: discord.Member):
        timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        roles = [role.mention for role in member.roles]
        embed = await utils.create_embed(f"{member.name}{member.discriminator}",
                                         f"{member.mention}")
        embed.set_image(url=member.avatar_url)
        embed.add_field(name="**Pending:**", value=f"{member.pending}", inline=True)
        embed.add_field(name='**Created account at:**', value=member.created_at.strftime(
            'Today at %-H:%M' if member.created_at.date() == datetime.today().date()
            else 'Yesterday at %-H:%M' if member.created_at.date() == (datetime.today() - timedelta(1)).date()
            else '%d-%m-%Y')
                        )
        embed.add_field(name="**Joined at:**", value=member.joined_at.strftime(
            'Today at %-H:%M' if member.joined_at.date() == datetime.today().date()
            else 'Yesterday at %-H:%M' if member.joined_at.date() == (datetime.today() - timedelta(1)).date()
            else '%d-%m-%Y')
                        )
        embed.add_field(name="**Roles:**", value=f"{roles}", inline=True)
        embed.set_footer(text=f"{timecurrentlyutc}")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.send_embed("Error",
                                   f"{ctx.author.mention} Please specify a user.",
                                   ctx,
                                   False)
        elif isinstance(error, commands.MemberNotFound):
            await utils.send_embed("Error",
                                   f"User is not in this server.",
                                   ctx,
                                   False)

    # reactionrole command

    @commands.command()
    @commands.has_role('Support Team')
    async def reactionrole(self, ctx):
        await utils.send_embed("Reaction Role Setup",
                               "Firstly, type the channel # you want to get the message to be sent in.",
                               ctx,
                               False)

        def check(m):
            return m.author.id == ctx.author.id

        chosen_channel = await self.bot.wait_for('message', check=check)
        if chosen_channel.content is not None:

            embed = await utils.create_embed("Reaction Role Setup",
                                             f"Alright, the message has been sent in {chosen_channel.content}. Please copy the message id and send it here.",
                                             )
            await ctx.send(embed=embed)
            channel_chosen_parsed = await commands.TextChannelConverter().convert(ctx, chosen_channel.content)
            embed = await utils.create_embed("**Roles**",
                                             f"React to this message to receive specific roles!,"
                                             )
            embed.add_field(name="Cybersecurity Expert",
                            value="React with :robot: to receive the Cybersecurity Expert role.", inline=False)
            embed.add_field(name="Ethical Hacker", value="React with :computer: to receive the Ethical Hacker role.",
                            inline=False)
            embed.add_field(name="Python Coder", value="React with :yellow_circle: to receive the Python Coder role.",
                            inline=False)
            embed.add_field(name="Notifications", value="React with :loudspeaker: to receive the Notifications role.",
                            inline=False)
            message_ = await channel_chosen_parsed.send(embed=embed)
            await message_.add_reaction("🤖")
            await asyncio.sleep(1)
            await message_.add_reaction("💻")
            await asyncio.sleep(1)
            await message_.add_reaction("🟡")
            await asyncio.sleep(1)
            await message_.add_reaction("📢")

            def check(m):
                return m.author.id == ctx.author.id

            chosen_messageid = await self.bot.wait_for('message', check=check)
            if chosen_messageid.content is not None:
                path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/reactionroles.json")
                with open(path, 'r') as f:
                    reactionroles = json.load(f)

                reactionroles[str(ctx.guild.id)] = f'{chosen_messageid.content}'

                with open(path, 'w') as f:
                    json.dump(reactionroles, f, indent=4)
                embed = await utils.create_embed("Reaction Role Setup",
                                                 f"The message id: {chosen_messageid.content} has been added to the list. Reacting should now add/remove roles.",
                                                 )
                await ctx.send(embed=embed)
            else:
                embed = await utils.create_embed("Error",
                                                 "An error has occured. Please try again.",
                                                 )
                await ctx.send(embed=embed)
        else:
            embed = await utils.create_embed("Error",
                                             "An error has occured. Please try again.",
                                             )
            await ctx.send(embed=embed)

    # ticket close command

    @commands.command()
    @commands.has_role('Support Team')
    async def close(self, ctx):
        if hasattr(ctx.message.channel, 'category'):
            if str(ctx.channel.category) == "Active Tickets" and ctx.author != self.bot.user:
                await ctx.message.delete()
                send_member = await commands.MemberConverter().convert(ctx, ctx.channel.name.split("-")[1])
                embed = await utils.create_embed("Ticket Closed",
                                                 "A staff member has closed your ticket. Sending a new message will create a new ticket, please only do so if you have a new issue.",
                                                 )
                if not send_member.dm_channel:
                    await send_member.create_dm()
                await send_member.dm_channel.send(embed=embed)
                embed = await utils.create_embed("Ticket Closed",
                                                 "Ticket will be deleted in 5 seconds...",
                                                 )
                await ctx.channel.send(embed=embed)
                transcript = await chat_exporter.export(ctx.channel, military_time=True)
                if transcript is None:
                    return
                transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                               filename=f"transcript-{ctx.channel.name}.html")
                transcript_channel: discord.TextChannel = discord.utils.get(ctx.guild.text_channels,
                                                                            name="ticket-transcripts")
                embed = await utils.create_embed()
                embed.set_author(name=f"{send_member.name}#{send_member.discriminator}",
                                 icon_url=f"{send_member.avatar.url}")
                embed.add_field(name="**Ticket Owner**", value=f"{send_member.mention}", inline=True)
                embed.add_field(name="**Ticket Owner ID**", value=f"{send_member.id}", inline=True)
                embed.add_field(name="**Ticket Name**", value=f"{ctx.channel.name}", inline=True)
                await transcript_channel.send(embed=embed, file=transcript_file)
                await asyncio.sleep(5)
                await ctx.channel.delete(reason="Ticket closed.")


async def setup(bot):
    await bot.add_cog(Staff(bot))
