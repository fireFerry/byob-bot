import datetime
import discord
import asyncio
from datetime import datetime
from discord.ext import commands
from config import config
import cogs.utils as utils


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # status command

    @commands.command(aliases=['version'])
    async def status(self, ctx):
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
    async def ping(self, ctx):
        await utils.send_embed("Ping",
                               f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms.",
                               ctx,)

    # GitHub command

    @commands.command(aliases=['gh'])
    async def github(self, ctx):
        await utils.send_embed("GitHub",
                               "This bot is open source, the project's source code can be found here: https://github.com/fireFerry/byob-bot",
                               ctx,)

    # issues command

    @commands.command()
    async def issues(self, ctx):
        await utils.send_embed("Issues",
                               "If you have any issues with the Byob Bot or suggestions for new features, let us know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,)

    # bugs command

    @commands.command()
    async def bugs(self, ctx):
        await utils.send_embed("Bugs",
                               "Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,)

    # Server stats update on join

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await utils.update_server_stats(member)

    # Server stats update on leave

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await utils.update_server_stats(member)

    # Give Member role after Membership Screening

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        autorolestatus, _ = await utils.autorole_status(after.guild.id)
        if autorolestatus == 'on':
            if before.pending != after.pending:
                role = discord.utils.get(before.guild.roles, name="Members")
                await after.add_roles(role)

    # help command

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        contents_name = ["General commands:",
                         "Support commands:",
                         "Staff commands:",
                         "Developer commands:"]
        contents_value = [
            "**$status|$version:** Displays the status of the bot.\n**$help:** Displays the commands list of the bot.\n**$ping:** Displays the latency of the bot.\n**$github:** Displays the GitHub link for the bot.\n**$issues:** Displays information if you have an issue or a feature request.\n**$bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n",
            "**$support:** Receiving help in the Discord.\n**$portforwarding|$portforward|$pfw:** Displays how to port forward.\n**$requirements|$req:** Displays the requirements needed for byob.\n**$wsl:** Displays information about using wsl for byob.\n**$vps:** Displays information about using byob on a vps.\n**$executable|$exe:** Displays information on what to do if executable payloads aren't generating.\n**$wiki:** Displays the wiki and GitHub links for BYOB",
            "**$contributor:** Toggle the Contributor role for a specific user.\n**$blacklist:** Toggle the Ticket Blacklist role for a specific user.**$userinfo|$ui:** Display informatiom about a specific user.\n**$toggleautorole:** Toggles whether the bot should give the Members role if member accepted membership screening.\n**$reactionrole:** Command to setup the reaction role system.",
            "**$shutdown:** Shutdown the bot completely.\n**$dev_status:** Information for the developer."]
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

        async def check(reactiongiven, userreacting):
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
