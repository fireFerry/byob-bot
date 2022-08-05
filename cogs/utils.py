import discord
import os
import json
emoji_roles = {
        '🤖': 'Cybersecurity Expert',
        '💻': 'Ethical Hacker',
        '🟡': 'Python Coder',
        '📢': 'Notifications',
    }


async def create_embed(title="", description="", color=0x5cffb0):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )
    return embed


async def send_embed(title, description, ctx=None, dmcommand=True, color=0x5cffb0):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )
    if dmcommand:
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
    else:
        await ctx.message.delete()
    await ctx.send(embed=embed)


async def update_server_stats(member):
    for channel in member.guild.voice_channels:
        if channel.name.startswith("Members:"):
            await channel.edit(name=f"Members: {len([m for m in member.guild.members if not m.bot])}")
        if channel.name.startswith("All Members:"):
            await channel.edit(name=f"All Members: {member.guild.member_count}")
        if channel.name.startswith("Bots:"):
            await channel.edit(name=f"Bots: {len([m for m in member.guild.members if m.bot])}")


async def autorole_status(guild_id):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/autorole.json")
    with open(path, 'r') as f:
        autoroles = json.load(f)
    autorolestatus = autoroles[f"{guild_id}"]
    return autorolestatus, autoroles


async def reactionrole_msgid(guild_id):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/reactionroles.json")
    with open(path, 'r') as f:
        reactionroles = json.load(f)
    msgid = reactionroles[f"{guild_id}"]
    return msgid


async def reactionrole_apply(payload=None, guild=None, apply_type="add"):
    if payload is None:
        return
    if apply_type == "add":
        if not payload.member or payload.member.bot:
            return
    if int(await reactionrole_msgid(guild.id)) == payload.message_id:
        name = emoji_roles[payload.emoji.name]
        member = discord.utils.get(guild.members, id=payload.user_id)
        if not member.dm_channel:
            await member.create_dm()
        if apply_type == "add":
            await member.add_roles(discord.utils.get(guild.roles, name=name))
            await member.dm_channel.send(f"You have been given the role **{name}**.")
        elif apply_type == "remove":
            await member.remove_roles(discord.utils.get(guild.roles, name=name))
            await member.dm_channel.send(f"You have been removed from the role **{name}**.")


async def togglerole(member: discord.Member, role: discord.Role, ctx):
    if role in member.roles:
        await member.remove_roles(role)
        await send_embed(f"{role.name}",
                         f"{member.mention} has been removed from the role **{role.name}**.",
                         ctx)
    else:
        await member.add_roles(role)
        await send_embed(f"{role.name}",
                         f"{member.mention} has been given the role **{role.name}**.",
                         ctx)
