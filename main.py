import os
import discord
import discord.ext
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def addrole(ctx, member : discord.Member, role : discord.Role):
    if role.name == 'Contributor':
        await member.add_roles(role)
        await ctx.message.delete()
        msg = f'Added the {role.name} role to {member.name}'
        await ctx.send(msg)
    else:
        await ctx.message.delete()
        msg = f"{ctx.author.mention}, You don't have the permission to add that role."
        await ctx.send(msg)
    

@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def delrole(ctx, member : discord.Member, role : discord.Role):
    if role.name == 'Contributor':
        await member.remove_roles(role)
        await ctx.message.delete()
        msg = f'Removed the {role.name} role from {member.name}'
        await ctx.send(msg)
    else:
        await ctx.message.delete()
        msg = f"{ctx.author.mention}, You don't have the permission to remove that role."
        await ctx.send(msg)

bot.run(TOKEN)
