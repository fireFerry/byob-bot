import datetime
import discord
import time
import asyncio

from datetime import timedelta, datetime
from discord.ext import commands
from config import config




class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['version'])
    async def status(self, ctx):
        embed = discord.Embed(title="Status",
                              description=f"**Status**: :green_circle: Running\n **Version**: {config.byob_bot_version}\n **Ping**: {round(self.bot.latency * 1000)}ms",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # commands list

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        contents_name = ["General commands:",
                         "Support commands:",
                         "Staff commands:",
                         "Developer commands:"]
        contents_value = [
            "**$status|$version:** Displays the status of the bot.\n**$help:** Displays the commands list of the bot.\n**$ping:** Displays the latency of the bot.\n**$github:** Displays the GitHub link for the bot.\n**$issues:** Displays information if you have an issue or a feature request.\n**$bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n**$joinrole EH/CE/PC:** Command to join one of the joinable roles by command.\n**$leaverole EH/CE/PC:** Command to leave one of the joinable roles by command.",
            "**$support:** Receiving help in the Discord.\n**$portforwarding|$portforward|$pfw:** Displays how to port forward.\n**$requirements|$req:** Displays the requirements needed for byob.\n**$wsl:** Displays information about using wsl for byob.\n**$vps:** Displays information about using byob on a vps.\n**$executable|$exe:** Displays information on what to do if executable payloads aren't generating.\n**$wiki:** Displays the wiki and GitHub links for BYOB",
            "**$addrole:** Add a role to a user.\n**$delrole:** Remove a role from a user.\n**$userinfo|$ui:** Display informatiom about a specific user.\n**$changeprefix:** Changes the prefix for the bot.\n**$toggleautorole:** Toggles wether the bot should give the Members role if member accepted membership screening.\n**$reactionrole:** Command to setup the reaction role system.",
            "**$shutdown:** Shutdown the bot completely.\n**$dev_status:** Information for the developer."]
        helppages = 3
        cur_page = 0
        timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S UTC")
        embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
        embed.add_field(name=f'{contents_name[cur_page]}', value=f'{contents_value[cur_page]}')
        embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
        message = await ctx.send(embed=embed)
        await message.add_reaction("\u25c0")
        await message.add_reaction("\u25b6")
        await message.add_reaction("\u23f9")

        def check(reactiongiven, userreacting):
            return userreacting == ctx.author and str(reactiongiven.emoji) in ["\u25c0", "\u25b6", "\u23f9"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "\u25b6" and cur_page != helppages:
                    cur_page += 1
                    embed.remove_field(0)
                    embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                    embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}",
                                    inline=False)
                    embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "\u25c0" and cur_page > 0:
                    cur_page -= 1
                    embed.remove_field(0)
                    embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                    embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}",
                                    inline=False)
                    embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "\u23f9":
                    cur_page = 0
                    embed.remove_field(0)
                    embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                    embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}",
                                    inline=False)
                    embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message):
            #with open('prefixes.json', 'r') as f:
                #prefixes = json.load(f)
            #currentprefix = config.prefix[f"{message.guild.id}"]
            embed = discord.Embed(title="Mentioned!",
                                  description=f"My prefix in this server: **{config.prefix}**\nHelp command: **{config.prefix}help**",
                                  color=0x5cffb0)
            await message.channel.send(embed=embed)
        await self.bot.process_commands(message)




def setup(bot):
    bot.add_cog(general(bot))