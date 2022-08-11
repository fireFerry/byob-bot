import discord.ui
from discord.ext import commands
import cogs.utils as utils


class RoleButtons(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Cybersecurity Expert", custom_id="cybersecurity-expert",
                       style=discord.ButtonStyle.blurple)
    async def cybersecurity_expert(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button, self.bot.get_guild(interaction.guild_id))

    @discord.ui.button(label="Ethical Hacker", custom_id="ethical-hacker",
                       style=discord.ButtonStyle.blurple)
    async def ethical_hacker(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button, self.bot.get_guild(interaction.guild_id))

    @discord.ui.button(label="Python Coder", custom_id="python-coder",
                       style=discord.ButtonStyle.blurple)
    async def python_coder(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button, self.bot.get_guild(interaction.guild_id))

    @discord.ui.button(label="Notifications", custom_id="notifications",
                       style=discord.ButtonStyle.blurple)
    async def notifications(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button, self.bot.get_guild(interaction.guild_id))


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RoleButtons(self.bot))


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
