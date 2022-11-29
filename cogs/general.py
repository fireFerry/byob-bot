import discord
import asyncio
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from config import config
import cogs.utils as utils


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # status command

    @commands.command(aliases=['version'])
    async def status(self, ctx: commands.Context):
        from cogs.prints import launch_time
        delta_uptime = datetime.utcnow() - launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime = str(f"{days}:{hours}:{minutes}:{seconds}")
        await utils.send_embed("Status",
                               f"**Status**: :green_circle: Running\n **Version**: {config.byob_bot_version}\n **Ping**: {round(self.bot.latency * 1000)}ms\n **Uptime**: {uptime}",
                               ctx,)

    # ping command

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await utils.send_embed("Ping",
                               f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms.",
                               ctx,)

    @app_commands.command(name="ping")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=await utils.create_embed("Ping", f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms."), ephemeral=True)

    # GitHub command


    @commands.command(aliases=['gh'])
    async def github(self, ctx: commands.Context):
        await utils.send_embed("GitHub",
                               "This bot is open source, the project's source code can be found here: https://github.com/fireFerry/byob-bot",
                               ctx,)

    # issues command

    @commands.command()
    async def issues(self, ctx: commands.Context):
        await utils.send_embed("Issues",
                               "If you have any issues with the Byob Bot or suggestions for new features, let us know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,)

    # bugs command

    @commands.command()
    async def bugs(self, ctx: commands.Context):
        await utils.send_embed("Bugs",
                               "Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,)

    # Server stats update on join

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.pending != after.pending and not after.pending:
            await utils.update_server_stats(after)

    # Server stats update on leave

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await utils.update_server_stats(member)

    # Give Member role after Membership Screening

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        autorolestatus, _ = await utils.autorole_status(after.guild.id)
        if autorolestatus == 'on':
            if before.pending != after.pending:
                await after.add_roles(discord.utils.get(before.guild.roles, name="Members"))

    # help command

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.message.delete()
        contents_name = ["General commands:",
                         "Support commands:",
                         "Staff commands:",
                         "Developer commands:"]
        contents_value = [
            f"**{config.prefix}status|{config.prefix}version:** Displays the status of the bot.\n**{config.prefix}help:** Displays the commands list of the bot.\n**{config.prefix}ping:** Displays the latency of the bot.\n**{config.prefix}github:** Displays the GitHub link for the bot.\n**{config.prefix}issues:** Displays information if you have an issue or a feature request.\n**{config.prefix}bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n",
            f"**{config.prefix}support:** Receiving help in the Discord.\n**{config.prefix}portforwarding|{config.prefix}portforward|{config.prefix}pfw:** Displays how to port forward.\n**{config.prefix}requirements|{config.prefix}req:** Displays the requirements needed for byob.\n**{config.prefix}wsl:** Displays information about using wsl for byob.\n**{config.prefix}vps:** Displays information about using byob on a vps.\n**{config.prefix}executable|{config.prefix}exe:** Displays information on what to do if executable payloads aren't generating.\n**{config.prefix}wiki:** Displays the wiki and GitHub links for BYOB",
            f"**{config.prefix}userinfo|{config.prefix}ui:** Display information about a specific user.\n**{config.prefix}contributor:** Toggle the Contributor role for a specific user.\n**{config.prefix}blacklist:** Toggle the Ticket Blacklist role for a specific user.**{config.prefix}userinfo|{config.prefix}ui:** Display information about a specific user.\n**{config.prefix}toggleautorole:** Toggles whether the bot should give the Members role if member accepted membership screening.\n**{config.prefix}reactionrole:** Command to setup the reaction role system.",
            f"**{config.prefix}shutdown:** Shutdown the bot completely.\n**{config.prefix}dev_status:** Information for the developer."]
        helppages = 3
        cur_page = 0
        timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S UTC")
        embed = await utils.create_embed(f"Help Page {cur_page + 1}/{helppages + 1}")
        embed.add_field(name=f'{contents_name[cur_page]}', value=f'{contents_value[cur_page]}')
        embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
        message = await ctx.send(embed=embed)
        await message.add_reaction("\u25c0")
        await message.add_reaction("\u25b6")
        await message.add_reaction("\u23f9")

        def check(reactiongiven, userreacting):
            return userreacting == ctx.author and str(reactiongiven.emoji) in ["\u25c0", "\u25b6", "\u23f9"]

        async def update_help(embed_message, helpmessage, current_page, help_pages):
            embed_message.remove_field(0)
            embed_message = await utils.create_embed(f"Help Page {current_page + 1}/{help_pages + 1}")
            embed_message.add_field(name=f"{contents_name[current_page]}",
                                    value=f"{contents_value[current_page]}",
                                    inline=False)
            embed_message.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
            await helpmessage.edit(embed=embed_message)
            await helpmessage.remove_reaction(reaction, user)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "\u25b6" and cur_page != helppages:
                    cur_page += 1
                    await update_help(embed, message, cur_page, helppages)
                elif str(reaction.emoji) == "\u25c0" and cur_page > 0:
                    cur_page -= 1
                    await update_help(embed, message, cur_page, helppages)
                elif str(reaction.emoji) == "\u23f9":
                    cur_page = 0
                    await update_help(embed, message, cur_page, helppages)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                return


async def setup(bot):
    await bot.add_cog(General(bot))
