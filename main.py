import os
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
version = '1.1'

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.message.delete
    msg = 'Byob Bot has been shut down.'
    await ctx.send(msg)
    await ctx.bot.logout()
    exit()


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.add_roles(role)
        await ctx.message.delete()
        msg = f'Added the {role.name} role to {member.name}'
        await ctx.send(msg)
    elif role.name == 'Ticket Blacklist:':
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
async def delrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.remove_roles(role)
        await ctx.message.delete()
        msg = f'Removed the {role.name} role from {member.name}'
        await ctx.send(msg)
    elif role.name == 'Ticket Blacklist':
        await member.remove_roles(role)
        await ctx.message.delete()
        msg = f'Removed the {role.name} role from {member.name}'
        await ctx.send(msg)
    else:
        await ctx.message.delete()
        msg = f"{ctx.author.mention}, You don't have the permission to remove that role."
        await ctx.send(msg)


@bot.command()
async def version(ctx):
    msg = f"I'm running on version {version}."


bot.run(TOKEN)
