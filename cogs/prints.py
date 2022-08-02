from datetime import datetime
from discord.ext import commands
launch_time = None


class Prints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} Joined the Guild')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member}Left the Guild')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            print(f"{message.guild}/{message.channel}/{message.author.name}>{message.content}")
            if message.embeds:
                print(message.embeds[0].to_dict())

    @commands.Cog.listener()
    async def on_ready(self):
        global launch_time
        launch_time = datetime.utcnow()
        print('User:', self.bot.user)
        print('ID:', self.bot.user.id)
        print('bot ready')


async def setup(bot):
    await bot.add_cog(Prints(bot))
