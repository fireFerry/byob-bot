from discord.ext import commands
import discord
import json
import os
from datetime import datetime, timedelta
import cogs.utils as utils
from cogs.reactionroles import RoleButtons


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # blacklist command

    @commands.command()
    @commands.has_role('Support Team')
    async def blacklist(self, ctx: commands.Context, member: discord.Member):
        await utils.togglerole(member, discord.utils.get(ctx.guild.roles, name="Ticket Blacklist"), ctx)

    # contributor command
    @commands.command()
    @commands.has_role('Support Team')
    async def contributor(self, ctx: commands.Context, member: discord.Member):
        await utils.togglerole(member, discord.utils.get(ctx.guild.roles, name="Contributor"), ctx)

    # toggleautorole command to toggle automatically giving the Member role after membership screening

    @commands.command()
    @commands.has_role('Support Team')
    async def toggleautorole(self, ctx: commands.Context):
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
    async def userinfo(self, ctx: commands.Context, member: discord.Member):
        timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        roles = [role.mention for role in member.roles]
        embed = await utils.create_embed(f"{member.name}{member.discriminator}",
                                         f"{member.mention}")
        embed.set_image(url=member.display_avatar.url)
        embed.add_field(name="**Pending:**", value=f"{member.pending}", inline=True)
        embed.add_field(name='**Created account at:**', value=member.created_at.strftime(
            'Today at %#H:%M' if member.created_at.date() == datetime.today().date()
            else 'Yesterday at %#H:%M' if member.created_at.date() == (datetime.today() - timedelta(1)).date()
            else '%d-%m-%Y at %#H:%M:%S')
                        )
        embed.add_field(name="**Joined at:**", value=member.joined_at.strftime(
            'Today at %#H:%M' if member.joined_at.date() == datetime.today().date()
            else 'Yesterday at %#H:%M' if member.joined_at.date() == (datetime.today() - timedelta(1)).date()
            else '%d-%m-%Y at %#H:%M:%S')
                        )
        embed.add_field(name="**Roles:**", value=f"{roles}", inline=True)
        embed.set_footer(text=f"{timecurrentlyutc}")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.send_embed("Error",
                                   f"{ctx.author.mention} Please specify a user.",
                                   ctx,
                                   False)
        elif isinstance(error, commands.MemberNotFound):
            await utils.send_embed("Error",
                                   "User is not in this server.",
                                   ctx,
                                   False)

    # reactionrole command

    @commands.command()
    @commands.has_role('Support Team')
    async def reactionrole(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = await utils.create_embed("**Roles**",
                                         "Click the buttons on this message to toggle roles and access special channels!"
                                         )
        message = await ctx.send(embed=embed, view=RoleButtons(self.bot))
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/reactionroles.json")
        with open(path, 'r') as f:
            reactionroles = json.load(f)
        reactionroles[str(ctx.guild.id)] = f'{message.id}'
        with open(path, 'w') as f:
            json.dump(reactionroles, f, indent=4)
        embed = await utils.create_embed("Button Role Setup",
                                         f"The message id: {message.id} has been added to the list.")
        await ctx.author.create_dm()
        await ctx.author.dm_channel.send(embed=embed)

    # ticket close command

    @commands.command()
    @commands.has_role('Support Team')
    async def close(self, ctx: commands.Context):
        if ctx.channel.type is discord.ChannelType.public_thread and ctx.channel.parent.name == "tickets" and ctx.author != self.bot.user:
            await ctx.message.delete()
            embed_dm = await utils.create_embed("Ticket Closed",
                                                "A staff member has closed your ticket. Sending a new message will create a new ticket, please only do so if you have a new issue.")
            ticket = await utils.get_ticket(thread_id=ctx.channel.id)
            send_dm = True
            if await utils.member_in_server(ctx.guild, ticket[0]):
                send_member = await commands.MemberConverter().convert(ctx, str(ticket[0]))
                embed = await utils.create_embed("Ticket Closed",
                                                 "Ticket will be deleted in 5 seconds...")
            else:
                send_member = await commands.UserConverter().convert(ctx, str(ticket[0]))
                send_dm = False
                embed = await utils.create_embed("Ticket Closed",
                                                 "Ticket closed because user left the server.")
            if send_dm:
                if not send_member.dm_channel:
                    await send_member.create_dm()
                await send_member.dm_channel.send(embed=embed_dm)
            await ctx.channel.send(embed=embed)
            await utils.close_ticket(ctx, send_member)

    # slash commands sync command

    @commands.command()
    @commands.has_role('Support Team')
    async def sync(self, ctx: commands.Context):
        await self.bot.tree.sync()
        await utils.send_embed("Slash Commands", "Slash commands synced.", ctx, False)


async def setup(bot):
    await bot.add_cog(Staff(bot))
