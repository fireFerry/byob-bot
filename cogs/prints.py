from discord.ext import commands
from config import config

class Prints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_member_join(member):
        print(f'{member} Joined the Guild')

    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f'{member}Left the Guild')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            print(f"{message.guild}/{message.channel}/{message.author.name}>{message.content}")
            if message.embeds:
                print(message.embeds[0].to_dict())

    @commands.Cog.listener()
    async def on_ready(self):
        if config.DEBUGGING == 1:
            print('Debugging')
        if config.DEBUGGING == 0:
            print('production')
        print('User:', self.bot.user)
        print('ID:', self.bot.user.id)
        print('bot ready')



def setup(bot):
    bot.add_cog(Prints(bot))