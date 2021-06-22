import os
import discord.ext
import datetime
import time
import json
import asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from datetime import timedelta, datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
byob_bot_version = '1.2.9'
intents = discord.Intents.default()
intents.members = True


# Gets the prefixes


def get_prefix(_, message):
    if message.guild is None:
        return "$"
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]


# Gets the on/off status for auto-role


def get_autorole(_, message):
    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)
    return autoroles[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)


# Loads the prefix into the json list


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '$'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)

    autoroles[str(guild.id)] = 'off'

    with open('prefixes.json', 'w') as f:
        json.dump(autoroles, f, indent=4)


# Removes the prefix from the json list


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)

    autoroles.pop(str(guild.id))

    with open('autorole.json', 'w') as f:
        json.dump(autoroles, f, indent=4)

    with open('reactionroles.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('reactionroles.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Changes the bot status to online and prints the bot name & id on start


@bot.event
async def on_ready():
    global launch_time
    launch_time = datetime.utcnow()
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="byob | $help"))
    print(bot.user.name)
    print(bot.user.id)


# Give role on reaction


@bot.event
async def on_raw_reaction_add(payload=None):
    if not payload.member.bot:
        try:
            with open('reactionroles.json', 'r') as f:
                reactionroles = json.load(f)
            msgid = reactionroles[f"{payload.guild_id}"]
        except KeyError:
            pass
        if int(msgid) is not None:
            guild = bot.get_guild(int(payload.guild_id))
            role_ce = discord.utils.get(guild.roles, name="Cybersecurity Expert")
            role_eh = discord.utils.get(guild.roles, name="Ethical Hacker")
            role_pc = discord.utils.get(guild.roles, name="Python Coder")
            role_no = discord.utils.get(guild.roles, name="Notifications")
            if payload is not None:
                if payload.message_id == int(msgid):
                    if str(payload.emoji) == "🤖":
                        await payload.member.add_roles(role_ce)
                    elif str(payload.emoji) == "💻":
                        await payload.member.add_roles(role_eh)
                    elif str(payload.emoji) == "🟡":
                        await payload.member.add_roles(role_pc)
                    elif str(payload.emoji) == "📢":
                        await payload.member.add_roles(role_no)


# Remove role if reaction removed


@bot.event
async def on_raw_reaction_remove(payload=None):
    try:
        with open('reactionroles.json', 'r') as f:
            reactionroles = json.load(f)
        msgid = reactionroles[f"{payload.guild_id}"]
    except KeyError:
        pass
    if int(msgid) is not None:
        guild = bot.get_guild(int(payload.guild_id))
        role_ce = discord.utils.get(guild.roles, name="Cybersecurity Expert")
        role_eh = discord.utils.get(guild.roles, name="Ethical Hacker")
        role_pc = discord.utils.get(guild.roles, name="Python Coder")
        role_no = discord.utils.get(guild.roles, name="Notifications")
        if payload is not None:
            if payload.message_id == int(msgid):
                if str(payload.emoji) == "🤖":
                    member = guild.get_member(int(payload.user_id))
                    await member.remove_roles(role_ce)
                elif str(payload.emoji) == "💻":
                    member = guild.get_member(int(payload.user_id))
                    await member.remove_roles(role_eh)
                elif str(payload.emoji) == "🟡":
                    member = guild.get_member(int(payload.user_id))
                    await member.remove_roles(role_pc)
                elif str(payload.emoji) == "📢":
                    member = guild.get_member(int(payload.user_id))
                    await member.remove_roles(role_no)


# Gives the Member role after membership screening


@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)
    autorolestatus = autoroles[f"{after.guild.id}"]
    if autorolestatus == 'on':
        if before.pending != after.pending:
            role = discord.utils.get(before.guild.roles, name="Members")
            await after.add_roles(role)


# Ignores "command not found" errors.


@bot.event
async def on_command_error(_, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


# respond on mention


@bot.event
async def on_message(message):
    if hasattr(message.channel, 'category'):
        if str(message.channel.category) == "Active tickets" and message.author != bot.user:
            ctx = await bot.get_context(message)
            send_member = await commands.MemberConverter().convert(ctx, message.channel.name)
            dm_channel = await send_member.create_dm()
            if str(message.attachments) != "[]":
                sent_attachment = await message.attachments[0].to_file(use_cached=False, spoiler=False)
                await dm_channel.send(content=message.content, file=sent_attachment)
            else:
                if message.content.startswith("$"):
                    await bot.process_commands(message)
                else:
                    await dm_channel.send(message.content)
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != bot.user:
        user = message.author
        guild_id = 817532239783919637
        support_server = bot.get_guild(guild_id)
        member = await support_server.fetch_member(user.id)

        match = False

        for channel in support_server.text_channels:
            await asyncio.sleep(0)

            if member.nick is not None:
                if channel.name == member.nick.lower():
                    match = True
                    if member.nick is None:
                        user_support = discord.utils.get(support_server.text_channels, name=member.name.lower())
                    else:
                        user_support = discord.utils.get(support_server.text_channels, name=member.nick.lower())
                    break
            else:
                if channel.name == member.name.lower():
                    match = True
                    if member.nick is None:
                        user_support = discord.utils.get(support_server.text_channels, name=member.name.lower())
                    else:
                        user_support = discord.utils.get(support_server.text_channels, name=member.nick.lower())
                    break

        if not match:

            support_category_name = 'Active tickets'
            support_category = discord.utils.get(support_server.categories, name=support_category_name)
            if member.nick is None:
                user_support = discord.utils.get(support_server.text_channels, name=member.name.lower())
            else:
                user_support = discord.utils.get(support_server.text_channels, name=member.nick.lower())

            if support_category is None:
                support_category_permissions = {
                    support_server.default_role: discord.PermissionOverwrite(send_messages=False)
                }
                await support_server.create_category(name=support_category_name,
                                                     overwrites=support_category_permissions)
                support_category = discord.utils.get(support_server.categories, name=support_category_name)
            if user_support is None:
                if member.nick is None:
                    await support_server.create_text_channel(name=member.name, category=support_category)
                else:
                    await support_server.create_text_channel(name=member.nick, category=support_category)

                user_support = discord.utils.get(support_server.text_channels, name=user.name.lower())
        if message.content.startswith("$"):
            await bot.process_commands(message)
        else:
            if str(message.attachments) != "[]":
                sent_attachment = await message.attachments[0].to_file(use_cached=False, spoiler=False)
                await user_support.send(content=message.content, file=sent_attachment)
            else:
                await user_support.send(message.content)

        # for guild in bot.guilds:
        #     for channel in guild.text_channels:
        #         if channel.name.startswith("bot-dm"):
        #             if not message.content.startswith("$"):
        #                 embed = discord.Embed(title=f"New message by {message.author.name}",
        #                                       description=f"{message.content}")
        #                 embed.set_author(name=f"{message.author.name}", icon_url=f"{message.author.avatar_url}")
        #                 embed.set_footer(text=f"ID: {message.author.id}")
        #                 await channel.send(embed=embed)
    else:
        await bot.process_commands(message)


# Change member count on join


@bot.event
async def on_member_join(member):
    for channel in member.guild.voice_channels:
        if channel.name.startswith("Members:"):
            await channel.edit(name=f"Members: {len([m for m in member.guild.members if not m.bot])}")
        if channel.name.startswith("All Members:"):
            await channel.edit(name=f"All Members: {member.guild.member_count}")
        if channel.name.startswith("Bots:"):
            await channel.edit(name=f"Bots: {len([m for m in member.guild.members if m.bot])}")


# Change member count on leave


@bot.event
async def on_member_remove(member):
    for channel in member.guild.voice_channels:
        if channel.name.startswith("Members:"):
            await channel.edit(name=f"Members: {len([m for m in member.guild.members if not m.bot])}")
        if channel.name.startswith("All Members:"):
            await channel.edit(name=f"All Members: {member.guild.member_count}")
        if channel.name.startswith("Bots:"):
            await channel.edit(name=f"Bots: {len([m for m in member.guild.members if m.bot])}")


# GENERAL COMMANDS

# status command to display the status of the bot


@bot.command(aliases=['version'])
async def status(ctx):
    delta_uptime = datetime.utcnow() - launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    uptime = str(f"{days}:{hours}:{minutes}:{seconds}")
    embed = discord.Embed(title="Status",
                          description=f"**Status**: :green_circle: Running\n **Version**: {byob_bot_version}\n **Ping**: {round(bot.latency * 1000)}ms\n **Uptime**: {uptime}",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# commands list


@bot.command()
async def help(ctx):
    await ctx.message.delete()
    contents_name = ["General commands:",
                     "Support commands:",
                     "Staff commands:",
                     "Developer commands:"]
    contents_value = [
        "**$status|$version:** Displays the status of the bot.\n**$help:** Displays the commands list of the bot.\n**$ping:** Displays the latency of the bot.\n**$github:** Displays the GitHub link for the bot.\n**$issues:** Displays information if you have an issue or a feature request.\n**$bugs:** Displays information on what to do if you have found a bug in Byob Bot.\n**$joinrole EH/CE/PC/NO:** Command to join one of the joinable roles by command.\n**$leaverole EH/CE/PC/NO:** Command to leave one of the joinable roles by command.",
        "**$support:** Receiving help in the Discord.\n**$portforwarding|$portforward|$pfw:** Displays how to port forward.\n**$requirements|$req:** Displays the requirements needed for byob.\n**$wsl:** Displays information about using wsl for byob.\n**$vps:** Displays information about using byob on a vps.\n**$executable|$exe:** Displays information on what to do if executable payloads aren't generating.\n**$wiki:** Displays the wiki and GitHub links for BYOB",
        "**$addrole:** Add a role to a user.\n**$delrole:** Remove a role from a user.\n**$userinfo|$ui:** Display informatiom about a specific user.\n**$changeprefix:** Changes the prefix for the bot.\n**$toggleautorole:** Toggles wether the bot should give the Members role if member accepted membership screening.\n**$reactionrole:** Command to setup the reaction role system.",
        "**$shutdown:** Shutdown the bot completely.\n**$dev_status:** Information for the developer."]
    helppages = 3
    cur_page = 0
    timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S UTC")
    embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
    embed.add_field(name=f'{contents_name[cur_page]}', value=f'{contents_value[cur_page]}')
    embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
    message = await ctx.send(embed=embed)
    await message.add_reaction("\u25c0")
    await message.add_reaction("\u25b6")
    await message.add_reaction("\u23f9")

    def check(reactiongiven, userreacting):
        return userreacting == ctx.author and str(reactiongiven.emoji) in ["\u25c0", "\u25b6", "\u23f9"]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            if str(reaction.emoji) == "\u25b6" and cur_page != helppages:
                cur_page += 1
                embed.remove_field(0)
                embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "\u25c0" and cur_page > 0:
                cur_page -= 1
                embed.remove_field(0)
                embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "\u23f9":
                cur_page = 0
                embed.remove_field(0)
                embed = discord.Embed(title=f"Help Page {cur_page + 1}/{helppages + 1}", color=0x5cffb0)
                embed.add_field(name=f"{contents_name[cur_page]}", value=f"{contents_value[cur_page]}", inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name} at {timecurrentlyutc}")
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break


# ping command


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping", description=f"Pong! Responded with a time of {round(bot.latency * 1000)}ms",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# github command


@bot.command()
async def github(ctx):
    embed = discord.Embed(title="Github",
                          description="This bot is open-source. The link to the project can be found here: https://github.com/fireFerry/byob-bot",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# issues command


@bot.command()
async def issues(ctx):
    embed = discord.Embed(title="Feature requests",
                          description="If you have any issues with the Byob Bot, or if you have a feature that you want added to the Byob Bot? Let me know! You can submit issues and feature requests here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# bugs command


@bot.command()
async def bugs(ctx):
    embed = discord.Embed(title="Bugs",
                          description="Do you think that you've found a bug with Byob Bot? No problem! Submit bug reports here: https://github.com/fireFerry/byob-bot/issues/new/choose",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# joinrole command


@bot.command()
async def joinrole(ctx, role):
    roletxt = str(role)
    if roletxt == "EH":
        role_eh = discord.utils.get(ctx.guild.roles, name="Ethical Hacker")
        await ctx.author.add_roles(role_eh)
        embed = discord.Embed(title="Role added", description=f"Added the {role_eh.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "CE":
        role_ce = discord.utils.get(ctx.guild.roles, name="Cybersecurity Expert")
        await ctx.author.add_roles(role_ce)
        embed = discord.Embed(title="Role added", description=f"Added the {role_ce.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "PC":
        role_pc = discord.utils.get(ctx.guild.roles, name="Python Coder")
        await ctx.author.add_roles(role_pc)
        embed = discord.Embed(title="Role added", description=f"Added the {role_pc.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "NO":
        role_no = discord.utils.get(ctx.guild.roles, name="Notifications")
        await ctx.author.add_roles(role_no)
        embed = discord.Embed(title="Role added", description=f"Added the {role_no.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description=f"{ctx.author.mention}, You don't have permission to join that role or an error occurred",
                              color=0x5cffb0)
        await ctx.send(embed=embed)


# leaverole command


@bot.command()
async def leaverole(ctx, role):
    roletxt = str(role)
    if roletxt == "EH":
        role_eh = discord.utils.get(ctx.guild.roles, name="Ethical Hacker")
        await ctx.author.remove_roles(role_eh)
        embed = discord.Embed(title="Role removed", description=f"Removed the {role_eh.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "CE":
        role_ce = discord.utils.get(ctx.guild.roles, name="Cybersecurity Expert")
        await ctx.author.remove_roles(role_ce)
        embed = discord.Embed(title="Role removed", description=f"Removed the {role_ce.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "PC":
        role_pc = discord.utils.get(ctx.guild.roles, name="Python Coder")
        await ctx.author.remove_roles(role_pc)
        embed = discord.Embed(title="Role removed", description=f"Removed the {role_pc.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == "NO":
        role_no = discord.utils.get(ctx.guild.roles, name="Notifications")
        await ctx.author.remove_roles(role_no)
        embed = discord.Embed(title="Role removed", description=f"Removed the {role_no.name} role",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error",
                              description=f"{ctx.author.mention}, You don't have permission to leave that role or an error occurred",
                              color=0x5cffb0)
        await ctx.send(embed=embed)


# SUPPORT COMMANDS

# support command


@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support",
                          description="**1.** Ask your question, don't ask to ask.\n**2.** Be patient for support. Don't mention staff, this will result in a punishment.\n**3.** Don't repeat your questions, and don't put them in multiple channels.",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# port forwarding command


@bot.command(aliases=['portforward', 'pfw'])
async def portforwarding(ctx):
    embed = discord.Embed(title="Port forwarding",
                          description="Port forwarding is done on your router, and may be called port mapping, or virtual servers too. Port triggering is not the same as port forwarding. \nTo use the web-gui version of byob you need to forward ports 1337-1339 to your machine that you're hosting byob on.",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# requirements command


@bot.command(aliases=['req'])
async def requirements(ctx):
    embed = discord.Embed(title="Requirements", description="requirements for byob:", color=0x5cffb0)
    embed.add_field(name="OS", value="A Linux distribution", inline=False)
    embed.add_field(name="Software", value="**1.** Python 3 & pip\n**2.** Docker", inline=False)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# wsl command


@bot.command()
async def wsl(ctx):
    embed = discord.Embed(title="Windows Subsystem for Linux",
                          description="Using wsl for byob isn't supported. This means that you will receive no support if you try to use byob with wsl. Wsl is if you run a linux terminal on Windows, also known as the Ubuntu/Kali from the Microsoft store.",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# vps command


@bot.command()
async def vps(ctx):
    embed = discord.Embed(title="Virtual Private Server",
                          description="Byob is not recommended on a vps. If you are using a vps for byob you may need to do some extra configuration with your vps provider. You also need to be able to open ports if you want to use byob, staff will not help with this.",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# executable command


@bot.command(aliases=['exe'])
async def executable(ctx):
    embed = discord.Embed(title="Executable generation",
                          description="If your executable doesn't generate correctly, here are some things you should check:\n**1.** Make sure you are using the latest version of byob and rebooted at least once.\n**2.** Run this command: sudo usermod -aG docker $USER && sudo chmod 666 /var/run/docker.sock, and reboot your system.\n**3.** If this still doesn't work, uninstall docker, and run startup.sh again, and reboot your system.\n**4.** If you tried all of this and it didn't help, you can try using pyinstaller to compile the python payload manually.",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# wiki command


@bot.command()
async def wiki(ctx):
    embed = discord.Embed(title="Wiki",
                          description="web-gui wiki: https://byob.dev/guide\ncli wiki: https://github.com/malwaredllc/byob/wiki\nGitHub: https://github.com/malwaredllc/byob/",
                          color=0x5cffb0)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    await ctx.send(embed=embed)


# STAFF COMMANDS

# addrole command to add a role to the user


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def addrole(ctx, member: discord.Member, role):
    roletxt = str(role)
    if roletxt == 'Contributor':
        role = discord.utils.get(ctx.guild.roles, name="Contributor")
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'Ticket Blacklist':
        role = discord.utils.get(ctx.guild.roles, name="Ticket Blacklist")
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'Members':
        role = discord.utils.get(ctx.guild.roles, name="Members")
        await member.add_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'EH':
        role_eh = discord.utils.get(ctx.guild.roles, name="Ethical Hacker")
        await member.add_roles(role_eh)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role_eh.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'PC':
        role_pc = discord.utils.get(ctx.guild.roles, name="Python Coder")
        await member.add_roles(role_pc)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role_pc.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'CE':
        role_ce = discord.utils.get(ctx.guild.roles, name="Cybersecurity Expert")
        await member.add_roles(role_ce)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role_ce.name} role to {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'NO':
        role_no = discord.utils.get(ctx.guild.roles, name="Notifications")
        await member.add_roles(role_no)
        await ctx.message.delete()
        embed = discord.Embed(title="Role added", description=f"Added the {role_no.name} role to {member.mention}",
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
async def delrole(ctx, member: discord.Member, role):
    roletxt = str(role)
    if roletxt == 'Contributor':
        role = discord.utils.get(ctx.guild.roles, name="Contributor")
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'Ticket Blacklist':
        role = discord.utils.get(ctx.guild.roles, name="Ticket Blacklist")
        await member.remove_roles(role)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed", description=f"Removed the {role.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'EH':
        role_eh = discord.utils.get(ctx.guild.roles, name="Ethical Hacker")
        await member.remove_roles(role_eh)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed",
                              description=f"Removed the {role_eh.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'PC':
        role_pc = discord.utils.get(ctx.guild.roles, name="Python Coder")
        await member.remove_roles(role_pc)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed",
                              description=f"Removed the {role_pc.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'CE':
        role_ce = discord.utils.get(ctx.guild.roles, name="Cybersecurity Expert")
        await member.remove_roles(role_ce)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed",
                              description=f"Removed the {role_ce.name} role from {member.mention}",
                              color=0x5cffb0)
        await ctx.send(embed=embed)
    elif roletxt == 'NO':
        role_no = discord.utils.get(ctx.guild.roles, name="Notifications")
        await member.remove_roles(role_no)
        await ctx.message.delete()
        embed = discord.Embed(title="Role removed",
                              description=f"Removed the {role_no.name} role from {member.mention}",
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


# toggleautorole command to toggle automatically giving the Member role after membership screening


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def toggleautorole(ctx):
    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)
    autorolestatus = autoroles[f"{ctx.guild.id}"]
    if autorolestatus == 'on':
        autoroles[str(ctx.guild.id)] = 'off'
        with open('autorole.json', 'w') as f:
            json.dump(autoroles, f, indent=4)
        await ctx.message.delete()
        embed = discord.Embed(title="Autorole toggled", description=f"Disabled autorole", color=0x5cffb0)
        await ctx.send(embed=embed)
    else:
        with open('autorole.json', 'r') as f:
            autoroles = json.load(f)
        autoroles[str(ctx.guild.id)] = 'on'
        with open('autorole.json', 'w') as f:
            json.dump(autoroles, f, indent=4)
        await ctx.message.delete()
        embed = discord.Embed(title="Autorole toggled", description=f"Enabled autorole", color=0x5cffb0)
        await ctx.send(embed=embed)


# userinfo command that displays information about the user.


@bot.command(pass_context=True, aliases=['ui'])
@commands.has_role('Support Team')
async def userinfo(ctx, member: discord.Member):
    timecurrentlyutc = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
    roles = [role.mention for role in member.roles]
    embed = discord.Embed(title=f"{member.name}{member.discriminator}", description=f"{member.mention}", color=0x5cffb0)
    embed.set_image(url=member.avatar_url)
    embed.add_field(name="**Pending:**", value=f"{member.pending}", inline=True)
    embed.add_field(name='**Created account at:**', value=member.created_at.strftime(
        'Today at %-H:%M' if member.created_at.date() == datetime.today().date()
        else 'Yesterday at %-H:%M' if member.created_at.date() == (datetime.today() - timedelta(1)).date()
        else '%d-%m-%Y')
                    )
    embed.add_field(name="**Joined at:**", value=member.joined_at.strftime(
        'Today at %-H:%M' if member.joined_at.date() == datetime.today().date()
        else 'Yesterday at %-H:%M' if member.joined_at.date() == (datetime.today() - timedelta(1)).date()
        else '%d-%m-%Y')
                    )
    embed.add_field(name="**Roles:**", value=f"{roles}", inline=True)
    embed.set_footer(text=f"{timecurrentlyutc}")
    await ctx.message.delete()
    await ctx.send(embed=embed)


# reactionrole command


@bot.command(pass_context=True)
@commands.has_role('Support Team')
async def reactionrole(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Reaction Role Setup",
                          description="Firstly, type the channel # you want to get the message to be sent in.",
                          color=0x60ffb0)
    await ctx.send(embed=embed)

    def check(m):
        return m.author.id == ctx.author.id

    chosen_channel = await bot.wait_for('message', check=check)
    if chosen_channel.content is not None:

        embed = discord.Embed(title="Reaction Role Setup",
                              description=f"Alright, the message has been sent in {chosen_channel.content}. Please copy the message id and send it here.",
                              color=0x60ffb0)
        await ctx.send(embed=embed)
        channel_chosen_parsed = await commands.TextChannelConverter().convert(ctx, chosen_channel.content)
        embed = discord.Embed(title="**Roles**", description="React to this message to receive specific roles!",
                              color=0x5cffb0)
        embed.add_field(name="Cybersecurity Expert",
                        value="React with :robot: to receive the Cybersecurity Expert role.", inline=False)
        embed.add_field(name="Ethical Hacker", value="React with :computer: to receive the Ethical Hacker role.",
                        inline=False)
        embed.add_field(name="Python Coder", value="React with :yellow_circle: to receive the Python Coder role.",
                        inline=False)
        embed.add_field(name="Notifications", value="React with :loudspeaker: to receive the Notifications role.",
                        inline=False)
        message_ = await channel_chosen_parsed.send(embed=embed)
        await message_.add_reaction("🤖")
        time.sleep(1)
        await message_.add_reaction("💻")
        time.sleep(1)
        await message_.add_reaction("🟡")
        time.sleep(1)
        await message_.add_reaction("📢")

        def check(m):
            return m.author.id == ctx.author.id

        chosen_messageid = await bot.wait_for('message', check=check)
        if chosen_messageid.content is not None:
            with open('reactionroles.json', 'r') as f:
                reactionroles = json.load(f)

            reactionroles[str(ctx.guild.id)] = f'{chosen_messageid.content}'

            with open('reactionroles.json', 'w') as f:
                json.dump(reactionroles, f, indent=4)
            embed = discord.Embed(title="Reaction Role Setup",
                                  description=f"The message id: {chosen_messageid.content} has been added to the list. Reacting should now add/remove roles.",
                                  color=0x60ffb0)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="An error occurred. Please try again.", color=0x60ffb0)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="An error occurred. Please try again.", color=0x60ffb0)
        await ctx.send(embed=embed)


# reply command


@bot.command()
@commands.has_role('Support Team')
async def close(ctx, *, message):
    if hasattr(ctx.message.channel, 'category'):
        if str(message.channel.category) == "Active tickets" and message.author != bot.user:
            send_member = await commands.MemberConverter().convert(ctx, message.channel.name)
            dm_channel = await send_member.create_dm()
            embed = discord.Embed(title="Ticket Closed",
                                  description="The support agent has closed the ticket. Sending a new message will open up a new ticket, so only do so if you have more questions.",
                                  color=0xc9cb65)
            await dm_channel.send(embed=embed)
            await ctx.message.delete()
            embed2 = discord.Embed(title="Ticket closed", description="Ticket will be deleted in 5 seconds...",
                                   color=0xaa5858)
            await ctx.send(embed=embed2)
            time.sleep(5)
            await ctx.channel.delete(reason="Ticket closed.")


# DEVELOPER COMMANDS

# shutdown command, only useable by the owner.


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.invisible)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    embed = discord.Embed(title="Shutdown", description=f"{bot.user.name} has been shut down.", color=0x5cffb0)
    await ctx.send(embed=embed)
    await bot.close()
    print(f'{bot.user.name} has been shut down.')


# dev-status command, only usable by the owner.


@bot.command()
@commands.is_owner()
async def dev_status(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    currentprefix = prefixes[f"{ctx.guild.id}"]
    with open('autorole.json', 'r') as f:
        autoroles = json.load(f)
    autorolestatus = autoroles[f"{ctx.guild.id}"]
    embed = discord.Embed(title="Dev Status",
                          description=f"**Status**: Running version {byob_bot_version}.\n**Ping**: {round(bot.latency * 1000)}ms\n**Prefix**: {currentprefix}\n**Autorole status**: {autorolestatus}",
                          color=0x5cffb0)
    embed.add_field(name="**Server stats**",
                    value=f"**Name**: {ctx.guild.name}\n**Members**: {ctx.guild.member_count}\n**Description**: {ctx.guild.description}",
                    inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)


bot.run(TOKEN)
