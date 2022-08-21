import io
from discord.ext import commands
import discord
import os
import json
import chat_exporter
import asyncio
from config import config

rolebuttons_roles = {
        'cybersecurity-expert': 'Cybersecurity Expert',
        'ethical-hacker': 'Ethical Hacker',
        'python-coder': 'Python Coder',
        'notifications': 'Notifications',
    }


async def create_embed(title: str = "", description: str = "", color=0x5cffb0):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )
    return embed


async def send_embed(title: str = "", description: str = "", ctx: commands.Context = None, dmcommand: bool = True, color=0x5cffb0):
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


async def update_server_stats(member: discord.Member):
    if member.guild.id == config.guild_id:
        for channel in member.guild.voice_channels:
            if channel.name.startswith("Members:"):
                await channel.edit(name=f"Members: {len([m for m in member.guild.members if not m.bot])}")
                await asyncio.sleep(5)
            if channel.name.startswith("All Members:"):
                await channel.edit(name=f"All Members: {member.guild.member_count}")
                await asyncio.sleep(5)
            if channel.name.startswith("Bots:") and member.bot:
                await channel.edit(name=f"Bots: {len([m for m in member.guild.members if m.bot])}")
                await asyncio.sleep(5)


async def autorole_status(guild_id: int):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/autorole.json")
    with open(path, 'r') as f:
        autoroles = json.load(f)
    autorolestatus = autoroles[f"{guild_id}"]
    return autorolestatus, autoroles


async def reactionrole_msgid(guild_id: int):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/reactionroles.json")
    with open(path, 'r') as f:
        reactionroles = json.load(f)
    msgid = reactionroles[f"{guild_id}"]
    return msgid


async def rolebuttons_apply(interaction: discord.Interaction, button: discord.Button, guild: discord.Guild):
    if int(await reactionrole_msgid(guild.id)) == interaction.message.id:
        if discord.utils.get(guild.roles, name=rolebuttons_roles[button.custom_id]) in interaction.user.roles:
            await interaction.user.remove_roles(discord.utils.get(guild.roles, name=rolebuttons_roles[button.custom_id]))
            await interaction.response.send_message(content=f"You have been removed from the role **{button.label}**.",
                                                    ephemeral=True)
        else:
            await interaction.user.add_roles(discord.utils.get(guild.roles, name=rolebuttons_roles[button.custom_id]))
            await interaction.response.send_message(content=f"You have been given the role **{button.label}**.",
                                                    ephemeral=True)


async def togglerole(member: discord.Member, role: discord.Role, ctx: commands.Context):
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


async def close_ticket(ctx: commands.Context, user):
    transcript = await chat_exporter.export(ctx.channel, military_time=True)
    if transcript is None:
        return
    transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                   filename=f"transcript-{ctx.channel.name}.html")
    transcript_channel: discord.TextChannel = discord.utils.get(ctx.guild.text_channels,
                                                                name="ticket-transcripts")
    embed = await create_embed()
    embed.set_author(name=f"{user.name}#{user.discriminator}",
                     icon_url=f"{user.display_avatar.url}")
    embed.add_field(name="**Ticket Owner**", value=f"{user.mention}", inline=True)
    embed.add_field(name="**Ticket Owner ID**", value=f"{user.id}", inline=True)
    embed.add_field(name="**Ticket Name**", value=f"{ctx.channel.name}", inline=True)
    await transcript_channel.send(embed=embed, file=transcript_file)
    await asyncio.sleep(5)
    await ctx.channel.delete(reason="Ticket closed.")


async def member_in_server(guild: discord.Guild, user_id: int):
    try:
        await guild.fetch_member(user_id)
        return True
    except discord.HTTPException:
        return False
