import os
import discord
import discord.ext
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
async def addrole(ctx, member : discord.Member, role : discord.Role):
    #user = ctx.message.author
    #role = discord.utils.get(user.server.roles, name="Contributor")
    await member.add_roles(role)


@bot.command(pass_context=True)
async def delrole(ctx, member : discord.Member, role : discord.Role):
    #user = ctx.message.author
    #role = discord.utils.get(user.server.roles, name="Contributor")
    await member.remove_roles(role)

token = "ODE3MTgyNDM4MzE1OTE3MzQ0.YEFycw.K-LVCjT0lQ2IA0P4uV-ett2Q2r4"
bot.run(token)
