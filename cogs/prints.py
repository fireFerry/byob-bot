import discord
from discord.ext import commands


class Prints(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f'{member} Joined the Guild')

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        print(f'{member}Left the Guild')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.bot.user.id:
            print(f"{message.guild}/{message.channel}/{message.author.name}>{message.content}")
            if message.embeds:
                print(message.embeds[0].to_dict())


async def setup(bot):
    await bot.add_cog(Prints(bot))
