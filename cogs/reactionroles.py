import discord.ui
from discord.ext import commands
import cogs.utils as utils


class RoleButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Cybersecurity Expert", custom_id="cybersecurity-expert",
                       style=discord.ButtonStyle.blurple)
    async def cybersecurity_expert(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button)

    @discord.ui.button(label="Ethical Hacker", custom_id="ethical-hacker",
                       style=discord.ButtonStyle.blurple)
    async def ethical_hacker(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button)

    @discord.ui.button(label="Python Coder", custom_id="python-coder",
                       style=discord.ButtonStyle.blurple)
    async def python_coder(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button)

    @discord.ui.button(label="Notifications", custom_id="notifications",
                       style=discord.ButtonStyle.blurple)
    async def notifications(self, interaction: discord.Interaction, button: discord.Button):
        await utils.rolebuttons_apply(interaction, button)


class RoleSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(cls=discord.ui.Select, options=[
        discord.SelectOption(label="Cybersecurity Expert", emoji="🦾"),
        discord.SelectOption(label="Ethical Hacker", emoji="🔐"),
        discord.SelectOption(label="Python Coder",  emoji="😎"),
        discord.SelectOption(label="Notifications", emoji="📢")
    ], custom_id="roleselect", placeholder="Select roles to apply!", min_values=0, max_values=4)
    async def role_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await utils.roleselect_apply(interaction, select)


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(RoleButtons())
        self.bot.add_view(RoleSelect())


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
