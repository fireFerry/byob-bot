import discord
import asyncio
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from config import config
import cogs.utils as utils


class HelpButtons(discord.ui.View):
    message_interaction = None

    def __init__(self):
        super().__init__(timeout=60)
        self.helppages = {
            "1": "General commands",
            "2": "Support commands",
            "3": "Staff commands",
            "4": "Developer commands"
        }
        self.helpmenu = {
            "General commands": f"**{config.prefix}status|{config.prefix}version:** Displays the status of the bot.\n**/help:** Displays the commands list of the bot.\n**/ping:** Displays the latency of the bot.\n**{config.prefix}github:** Displays the GitHub link for the bot.\n**{config.prefix}issues:** Displays information if you have an issue or a feature request.\n**{config.prefix}bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n",
            "Support commands": f"**{config.prefix}support:** Receiving help in the Discord.\n**{config.prefix}portforwarding|{config.prefix}portforward|{config.prefix}pfw:** Displays how to port forward.\n**{config.prefix}requirements|{config.prefix}req:** Displays the requirements needed for byob.\n**{config.prefix}wsl:** Displays information about using wsl for byob.\n**{config.prefix}vps:** Displays information about using byob on a vps.\n**{config.prefix}executable|{config.prefix}exe:** Displays information on what to do if executable payloads aren't generating.\n**{config.prefix}wiki:** Displays the wiki and GitHub links for BYOB",
            "Staff commands": f"**{config.prefix}userinfo|{config.prefix}ui:** Display information about a specific user.\n**{config.prefix}contributor:** Toggle the Contributor role for a specific user.\n**{config.prefix}blacklist:** Toggle the Ticket Blacklist role for a specific user.**{config.prefix}userinfo|{config.prefix}ui:** Display information about a specific user.\n**{config.prefix}toggleautorole:** Toggles whether the bot should give the Members role if member accepted membership screening.\n**{config.prefix}reactionrole:** Command to setup the reaction role system.",
            "Developer commands": f"**{config.prefix}shutdown:** Shutdown the bot completely.\n**{config.prefix}dev_status:** Information for the developer."
        }
        self.current_page = 1
        self.pages_total = 4

    async def update_help(self, interaction: discord.Interaction):
        await interaction.message.edit(embed=await utils.create_embed(f"{self.helppages[f'{self.current_page}']}: {self.current_page}/{self.pages_total}",
                                                                      self.helpmenu[self.helppages[str(self.current_page)]],
                                                                      author=interaction.user),
                                       view=self)
        await interaction.response.defer()

    async def on_timeout(self) -> None:
        self.clear_items()
        self.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="◀️", disabled=True))
        self.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏹️", disabled=True))
        self.add_item(item=discord.ui.Button(style=discord.ButtonStyle.primary, emoji="▶️", disabled=True))
        await HelpButtons.message_interaction.edit_original_response(view=self)

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="back", emoji="◀️", disabled=True)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.forward.disabled = False
        if self.current_page != 1:
            self.current_page -= 1
        if self.current_page == 1:
            self.reset.disabled = True
            button.disabled = True
        await self.update_help(interaction)

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="reset", emoji="⏹️", disabled=True)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.back.disabled = True
        self.forward.disabled = False
        self.current_page = 1
        await self.update_help(interaction)

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="forward", emoji="▶️")
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.back.disabled = False
        self.reset.disabled = False
        if self.current_page != self.pages_total:
            self.current_page += 1
        if self.current_page == self.pages_total:
            button.disabled = True
        await self.update_help(interaction)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # status command

    @commands.command(aliases=['version'])
    async def status(self, ctx: commands.Context):
        from cogs.basic import launch_time
        uptime = datetime.timestamp(launch_time)
        await utils.send_embed("Status",
                               f"**Status**: :green_circle: Running\n **Version**: {config.byob_bot_version}\n **Ping**: {round(self.bot.latency * 1000)}ms\n **Online since**: <t:{uptime.__floor__()}:R>",
                               ctx,
                               author=ctx.author)

    # ping command

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await utils.send_embed("Ping",
                               f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms.",
                               ctx,
                               author=ctx.author)

    @app_commands.command(name="ping", description="Displays the latency of the bot.")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=await utils.create_embed("Ping", f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms.", author=interaction.user))

    # GitHub command

    @commands.command(aliases=['gh'])
    async def github(self, ctx: commands.Context):
        await utils.send_embed("GitHub",
                               "This bot is open source, the project's source code can be found here: https://github.com/fireFerry/byob-bot",
                               ctx,
                               author=ctx.author)

    # issues command

    @commands.command()
    async def issues(self, ctx: commands.Context):
        await utils.send_embed("Issues",
                               "If you have any issues with the Byob Bot or suggestions for new features, let us know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,
                               author=ctx.author)

    # bugs command

    @commands.command()
    async def bugs(self, ctx: commands.Context):
        await utils.send_embed("Bugs",
                               "Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                               ctx,
                               author=ctx.author)

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
        await message.add_reaction("\u23f9")
        await message.add_reaction("\u25b6")

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

    @app_commands.command(name="help", description="Displays the commands list of the bot.")
    async def help_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=await utils.create_embed("General commands: 1/4", f"**{config.prefix}status|{config.prefix}version:** Displays the status of the bot.\n**/help:** Displays the commands list of the bot.\n**/ping:** Displays the latency of the bot.\n**{config.prefix}github:** Displays the GitHub link for the bot.\n**{config.prefix}issues:** Displays information if you have an issue or a feature request.\n**{config.prefix}bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n",
                                                                               author=interaction.user),
                                                view=HelpButtons())
        HelpButtons.message_interaction = interaction


async def setup(bot):
    await bot.add_cog(General(bot))
