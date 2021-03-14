import os
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
byob_bot_version = '1.2'

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
    await ctx.message.delete()
    embed = discord.Embed(title="Shutdown", description="Byob Bot has been shut down.", color=0x5cffb0)
    await ctx.send(embed=embed)
    await ctx.bot.logout()
    print('Byob Bot has been shut down.')


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}", color=0x5cffb0)
        await ctx.send(embed=embed)
    elif role.name == 'Ticket Blacklist':
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}", color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You don't have permission to add that role.", color=0x5cffb0)
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def delrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}", color=0x5cffb0)
        await ctx.send(embed=embed)
    elif role.name == 'Ticket Blacklist':
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}", color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="Error", description=f"{ctx.author.mention}, You don't have permission to remove that role.", color=0x5cffb0)
        await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    embed = discord.Embed(title="Status", description=f"**Status**: :green_circle: Running\n **Version**: {byob_bot_version}\n **Ping**: {round(bot.latency * 1000)}ms", color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


bot.run(TOKEN)
