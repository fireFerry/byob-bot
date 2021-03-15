import os
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
byob_bot_version = '1.2.1'

bot = commands.Bot(command_prefix='$', help_command=None)

# changes the bot status to online and prints the bot name & id on start


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="byob | $commands"))
    print(bot.user.name)
    print(bot.user.id)

# shutdown command, only useable by the owner.


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.message.delete()
    embed = discord.Embed(title="Shutdown", description="Byob Bot has been shut down.", color=0x5cffb0)
    await ctx.send(embed=embed)
    await ctx.bot.logout()
    print('Byob Bot has been shut down.')


# addrole command to add a role to the user


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

# delrole command to remove a role from the user


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

# status command to display the status of the bot


@bot.command()
async def status(ctx):
    embed = discord.Embed(title="Status", description=f"**Status**: :green_circle: Running\n **Version**: {byob_bot_version}\n **Ping**: {round(bot.latency * 1000)}ms", color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping", description=f"Pong! Responded with a time of {round(bot.latency * 1000)}ms", color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)

# port forwarding command


@bot.command()
async def portforwarding(ctx):
    embed = discord.Embed(title="Port forwarding", description="Port forwarding is done on your router, and may be called port mapping, or virtual servers too. Port triggering is not the same as port forwarding. \nTo use the web-gui version of byob you need to forward ports 1337-1339 to your machine that you're hosing byob on.", color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# support command

@bot.command(aliases=['help'])
async def support(ctx):
    embed = discord.Embed(title="Support", description="**1.** Ask your question, don't ask to ask.\n**2. **Be patient for support. Don't mention staff, this will result in a punishment.\n**3.**Don't repeat your questions, and don't put them in multiple channels.", color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)

# requirements command


@bot.command()
async def requirements(ctx):
    embed = discord.Embed(title="Requirements",  escription="requirements for byob:", color=0x5cffb0)
    embed.add_field(name="OS", value="A Linux distribution", inline=False)
    embed.add_field(name="Software", value="**1.** Python 3 & pip\n**2.** Docker", inline=False)
    await ctx.mesasge.delete()
    await ctx.send(embed=embed)


# commands list

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Commands", description="These are my commands:", color=0x5cffb0)
    embed.add_field(name="General commands:", value="**$status:** Displays the status of the bot.\n**$commands:** Displays the commands list of the bot.\n**$ping:** Displays the latency of the bot.", inline=False)
    embed.add_field(name="Support commands:", value="**$support|$help:** Receiving help in the Discord.\n**$portforwarding:** Displays how to port forward.\n**$requirements:** Displays the requirements needed for byob.", inline=False)
    embed.add_field(name="Staff commands:", value="**$addrole:** Add a role to a user.\n**$delrole:** Remove a role from a user.", inline=False)
    embed.add_field(name="Developer commands:", value="**$shutdown:** Shutdown the bot completely.", inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


bot.run(TOKEN)
