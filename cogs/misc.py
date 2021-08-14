from discord.ext import commands
import discord


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ping command

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Ping", description=f"Pong! Responded with a time of {round(self.bot.latency * 1000)}ms",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # github command

    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(title="Github",
                              description="This bot is open-source. The link to the project can be found here: https://github.com/fireFerry/byob-bot",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # issues command

    @commands.command()
    async def issues(self, ctx):
        embed = discord.Embed(title="Feature requests",
                              description="If you have any issues with the Byob Bot, or if you have a feature that you want added to the Byob Bot? Let me know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    # bugs command

    @commands.command()
    async def bugs(self, ctx):
        embed = discord.Embed(title="Bugs",
                              description="Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                              color=0x5cffb0)
        await ctx.message.delete()
        await ctx.send(embed=embed)






def setup(bot):
    bot.add_cog(misc(bot))