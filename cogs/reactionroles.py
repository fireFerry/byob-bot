from discord.ext import commands
import cogs.utils as utils


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Give role on reaction

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload=None):
        await utils.reactionrole_apply(payload, self.bot.get_guild(payload.guild_id), "add")

    # Remove role if reaciton removed

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload=None):
        await utils.reactionrole_apply(payload, self.bot.get_guild(payload.guild_id), "remove")


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
