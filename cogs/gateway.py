import discord
from discord.ext import commands
from config import config
import cogs.utils as utils
from datetime import datetime, timedelta


class Gateway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.roles != after.roles and after.guild.id == config.gateway_guild_id:
            if discord.utils.get(after.guild.roles, name="Verified") in after.roles:
                channel = await self.bot.get_guild(config.guild_id).fetch_channel(config.rules_channel_id)
                invite = await channel.create_invite(
                    max_age=600,
                    max_uses=1,
                    temporary=True,
                    unique=True,
                    reason=f"{after.name}#{after.discriminator} has passed verification in gateway server")
                await after.create_dm()
                await after.dm_channel.send(embed=await utils.create_embed("Verified",
                                                                           f"You have verified yourself in the gateway server, please join {invite.url}"))
                embed = await utils.create_embed("Verified",
                                                 f"{after} has verified themselves and has received an invite to the server.")
                channel = await self.bot.get_guild(config.gateway_guild_id).fetch_channel(config.gateway_log_channel_id)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == config.guild_id:
            try:
                await self.bot.get_guild(config.gateway_guild_id).fetch_member(member.id)
            except discord.DiscordException:
                if not member.dm_channel:
                    await member.create_dm()
                await member.dm_channel.send(embed=await utils.create_embed("Error",
                                                                            "You are not verified in the gateway server. Please join the gateway server and verify yourself."))
                await member.guild.kick(member, reason="User joined server without using gateway invite.")
                return
            await self.bot.get_guild(config.gateway_guild_id).kick(member, reason="User joined main server.")
            log_channel = await self.bot.get_guild(config.gateway_guild_id).fetch_channel(config.gateway_log_channel_id)
            await log_channel.send(embed=await utils.create_embed("Member joined main server",
                                                                  f"{member} has joined the main server and has been kicked from the gateway server."))
        if member.guild.id == config.gateway_guild_id:
            if self.bot.get_guild(config.guild_id) in member.mutual_guilds:
                if not member.dm_channel:
                    await member.create_dm()
                await member.dm_channel.send(embed=await utils.create_embed("Error",
                                                                            "You cannot join the gateway server while being in the main server."))
                await member.kick(reason="User is in main server.")
                log_channel = await member.guild.fetch_channel(config.gateway_log_channel_id)
                await log_channel.send(embed=await utils.create_embed("Rejected server join",
                                                                      f"{member} tried to join the gateway server while being in the main server, and has been kicked."))
                return
            embed = await utils.create_embed(description=f"{member.mention} joined")
            embed.set_author(name=member, icon_url=member.avatar.url)
            embed.add_field(name="Name", value=f"{member} ({member.id}) {member.mention}", inline=False)
            embed.add_field(name='**Created account at:**', value=member.created_at.strftime(
                'Today at %#H:%M:%S' if member.created_at.date() == datetime.today().date()
                else 'Yesterday at %#H:%M:%S' if member.created_at.date() == (datetime.today() - timedelta(1)).date()
                else '%d-%m-%Y at %#H:%M:%S')
                            )
            embed.add_field(name="**Joined at:**", value=member.joined_at.strftime(
                'Today at %#H:%M:%S' if member.joined_at.date() == datetime.today().date()
                else 'Yesterday at %#H:%M:%S' if member.joined_at.date() == (datetime.today() - timedelta(1)).date()
                else '%d-%m-%Y at %-#H:%M:%S')
                            )
            channel = await member.guild.fetch_channel(config.gateway_log_channel_id)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, _, member: discord.Member):
        if member.guild.id == config.guild_id:
            await self.bot.get_guild(config.gateway_guild_id).ban(member.id, reason="User banned from main server, synchronizing bans.")

    @commands.Cog.listener()
    async def on_member_unban(self, _, member: discord.Member):
        if member.guild.id == config.guild_id:
            await self.bot.get_guild(config.gateway_guild_id).unban(member.id, reason="User unbanned from main server, synchronizing unbans.")


async def setup(bot):
    await bot.add_cog(Gateway(bot))
