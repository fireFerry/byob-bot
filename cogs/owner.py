import discord.ext
import json
from discord.ext import commands
from config import config

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # DEVELOPER COMMANDS

    # shutdown command, only useable by the owner.


    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.change_presence(status=discord.Status.invisible)
        await ctx.message.delete()
        embed = discord.Embed(title="Shutdown", description=f"{self.bot.user} has been shut down.", color=0x5cffb0)
        await ctx.send(embed=embed)
        print(f'{self.bot.user} has been shut down.')


    # dev-status command, only usable by the owner.


    @commands.command()
    @commands.is_owner()
    async def dev_status(self, ctx):
        #with open('autorole.json', 'r') as f:
            ##autoroles = json.load(f)
        #autorolestatus = autoroles[f"{ctx.guild.id}"]
        embed = discord.Embed(title="Dev Status",
                              description=f"**Status**: Running version {config.byob_bot_version}.\n**Ping**: {round(self.bot.latency * 1000)}ms\n**Prefix**: {config.prefix}\n**Autorole status**: {'autorolestatus'}", color=0x5cffb0)
        embed.add_field(name="**Server stats**",
                        value=f"**Name**: {ctx.guild.name}\n**Members**: {ctx.guild.member_count}\n**Description**: {ctx.guild.description}",
                        inline=False)
        await ctx.message.delete()
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(owner(bot))