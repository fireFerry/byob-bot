import os
import discord.ext
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
byob_bot_version = '1.2.4'
intents = discord.Intents.default()
intents.members = True


# Gets the prefixes


def get_prefix(_, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)


# Loads the prefix into the json list


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Removes the prefix from the json list


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Changes the bot status to online and prints the bot name & id on start


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="byob | $help"))
    print(bot.user.name)
    print(bot.user.id)


# Gives the Member role after membership screening


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.pending != after.pending:
        role = discord.utils.get(before.guild.roles, name="Members")
        await after.add_roles(role)


# Ignores "command not found" errors.


@bot.event
async def on_command_error(_, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


# GENERAL COMMANDS

# status command to display the status of the bot


@bot.command(aliases=['version'])
async def status(ctx):
    embed = discord.Embed(title="Status",
                          description=f"**Status**: :green_circle: Running\n **Version**: {byob_bot_version}\n **Ping**: {round(bot.latency * 1000)}ms",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# commands list


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Commands", description="These are my commands:", color=0x5cffb0)
    embed.add_field(name="General commands:",
                    value="**$status|$version:** Displays the status of the bot.\n**$help:** Displays the commands list of the bot.\n**$ping:** Displays the latency of the bot.\n**$github:** Displays the GitHub link for the bot.\n**$issues:** Displays information if you have an issue or a feature request.\n**$bugs:** Displays information on what to do if you've found a bug in Byob Bot.",
                    inline=False)
    embed.add_field(name="Support commands:",
                    value="**$support:** Receiving help in the Discord.\n**$portforwarding:** Displays how to port forward.\n**$requirements:** Displays the requirements needed for byob.\n**$wsl:** Displays information about using wsl for byob.\n**$vps:** Displays information about using byob on a vps.",
                    inline=False)
    embed.add_field(name="Staff commands:",
                    value="**$addrole:** Add a role to a user.\n**$delrole:** Remove a role from a user.", inline=False)
    embed.add_field(name="Developer commands:", value="**$shutdown:** Shutdown the bot completely.", inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# ping command


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping", description=f"Pong! Responded with a time of {round(bot.latency * 1000)}ms",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# github command


@bot.command()
async def github(ctx):
    embed = discord.Embed(title="Github",
                          description="This bot is open-source. The link to the project can be found here: https://github.com/fireFerry/byob-bot",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# issues command


@bot.command()
async def issues(ctx):
    embed = discord.Embed(title="Feature requests",
                          description="If you have any issues with the Byob Bot, or if you have a feature that you want added to the Byob Bot? Let me know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# bugs command


@bot.command()
async def bugs(ctx):
    embed = discord.Embed(title="Bugs",
                          description="Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# SUPPORT COMMANDS

# support command


@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support",
                          description="**1.** Ask your question, don't ask to ask.\n**2.** Be patient for support. Don't mention staff, this will result in a punishment.\n**3.** Don't repeat your questions, and don't put them in multiple channels.",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# port forwarding command


@bot.command()
async def portforwarding(ctx):
    embed = discord.Embed(title="Port forwarding",
                          description="Port forwarding is done on your router, and may be called port mapping, or virtual servers too. Port triggering is not the same as port forwarding. \nTo use the web-gui version of byob you need to forward ports 1337-1339 to your machine that you're hosing byob on.",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# requirements command


@bot.command()
async def requirements(ctx):
    embed = discord.Embed(title="Requirements", description="requirements for byob:", color=0x5cffb0)
    embed.add_field(name="OS", value="A Linux distribution", inline=False)
    embed.add_field(name="Software", value="**1.** Python 3 & pip\n**2.** Docker", inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# wsl command


@bot.command()
async def wsl(ctx):
    embed = discord.Embed(title="Windows Subsystem for Linux",
                          description="Using wsl for byob isn't supported. This means that you will receive no support if you try to use byob with wsl. Wsl is if you run a linux terminal on Windows, also known as the Ubuntu/Kali from the Microsoft store.",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# vps command


@bot.command()
async def vps(ctx):
    embed = discord.Embed(title="Virtual Private Server",
                          description="Byob is not recommended on a vps. If you are using a vps for byob you may need to do some extra configuration with your vps provider. You also need to be able to open ports if you want to use byob, staff will not help with this.",
                          color=0x5cffb0)
    await ctx.message.delete()
    await ctx.send(embed=embed)


# STAFF COMMANDS

# addrole command to add a role to the user


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif role.name == 'Ticket Blacklist':
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="Error",
                              description=f"{ctx.author.mention}, You don't have permission to add that role.",
                              color=0x5cffb0)
        await ctx.send(embed=embed)


# delrole command to remove a role from the user


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def delrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == 'Contributor':
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif role.name == 'Ticket Blacklist':
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        embed = discord.Embed(title="Error",
                              description=f"{ctx.author.mention}, You don't have permission to remove that role.",
                              color=0x5cffb0)
        await ctx.send(embed=embed)


# changeprefix command to change the prefix of the bot.


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.message.delete()
    embed = discord.Embed(title="Prefix changed", description=f"Prefix changed to: {prefix}", color=0x5cffb0)
    await ctx.send(embed=embed)


# DEVELOPER COMMANDS

# shutdown command, only useable by the owner.


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.invisible)
    await ctx.message.delete()
    embed = discord.Embed(title="Shutdown", description="Byob Bot has been shut down.", color=0x5cffb0)
    await ctx.send(embed=embed)
    await bot.close()
    print(f'{bot.user.name} has been shut down.')


bot.run(TOKEN)
