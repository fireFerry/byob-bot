import discord
from discord.ext import commands
from datetime import datetime, timedelta
from config import config

launch_time, bot_name, bot_avatar = None, None, None


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global launch_time, bot_avatar, bot_name
        bot_avatar, bot_name = self.bot.user.avatar.url, self.bot.user.name
        launch_time = datetime.utcnow() + timedelta(hours=1)
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=f"byob | {config.prefix}help"))
        print(f"User: {self.bot.user}\nID: {self.bot.user.id}\nBot ready!")


async def setup(bot):
    await bot.add_cog(Basic(bot))
