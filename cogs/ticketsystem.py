import discord
from discord.ext import commands
from config import config
import cogs.utils as utils


class CloseButton(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", custom_id="close", style=discord.ButtonStyle.red)
    async def close_button(self, interaction: discord.Interaction, button: discord.Button):
        ctx = await self.bot.get_context(interaction.message)
        embed_dm = await utils.create_embed("Ticket Closed",
                                            "A staff member has closed your ticket. Sending a new message will create a new ticket, please only do so if you have a new issue.")
        if await utils.member_in_server(interaction.guild, ctx.channel.name.split("-")[1]):
            send_member = await commands.MemberConverter().convert(ctx, ctx.channel.name.split("-")[1])
            embed = await utils.create_embed("Ticket Closed",
                                             "Ticket will be deleted in 5 seconds...", )
            embed_dm = False
        else:
            send_member = await commands.UserConverter().convert(ctx, ctx.channel.name.split("-")[1])
            embed = await utils.create_embed("Ticket Closed",
                                             "Ticket closed because user left the server.")
        if embed_dm is discord.Embed:
            if not send_member.dm_channel:
                await send_member.create_dm()
            await send_member.dm_channel.send(embed=embed_dm)
        button.label = "Closed"
        button.disabled = True
        await interaction.response.send_message(embed=embed, view=self)
        await utils.close_ticket(ctx, send_member)
        self.stop()


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CloseButton(self.bot))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if hasattr(message.channel, 'category') and str(message.channel.category) == "Active Tickets":
            if message.guild.id != config.guild_id or message.content == f"{config.prefix}close":
                return
            if not await utils.member_in_server(message.guild, int(message.channel.name.split("-")[1])):
                send_member: discord.User = await commands.UserConverter().convert(await self.bot.get_context(message), message.channel.name.split("-")[1])
                embed = await utils.create_embed("Ticket Closed", "Ticket closed because user left the server.")
                await message.channel.send(embed=embed)
                await utils.close_ticket(await self.bot.get_context(message), send_member)
                return
            send_member: discord.Member = await commands.MemberConverter().convert(await self.bot.get_context(message), message.channel.name.split("-")[1])
            if not send_member.dm_channel:
                await send_member.create_dm()
            if str(message.attachments) != "[]":
                sent_attachment = await message.attachments[0].to_file(use_cached=False, spoiler=False)
                await send_member.dm_channel.send(content=message.content, file=sent_attachment)
            else:
                await send_member.dm_channel.send(message.content)
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.content.startswith(config.prefix) or self.bot.get_guild(config.gateway_guild_id) in message.author.mutual_guilds:
                await self.bot.process_commands(message)
                return
            support_server = self.bot.get_guild(config.guild_id)
            member = await support_server.fetch_member(message.author.id)
            if discord.utils.get(support_server.roles, name="Ticket Blacklist") in member.roles:
                embed = await utils.create_embed("Ticket Blacklisted",
                                                 "You are blacklisted from creating tickets. Please contact a staff member if you think this is in error.",)
                await message.author.send(embed=embed)
                return
            match = None
            for channel in support_server.text_channels:
                if channel.name.startswith("ticket-") and channel.name.split("-")[1] == str(member.id):
                    match = channel
                    break
            user_support_channel: discord.TextChannel = match
            if not match:
                support_category = discord.utils.get(support_server.categories, name="Active Tickets")
                if support_category is None:
                    raise commands.ChannelNotFound("Category 'Active Tickets' not found")
                user_support_channel: discord.TextChannel = await support_server.create_text_channel(name=f"ticket-{member.id}", category=support_category)
                embed = await utils.create_embed("Ticket Opened",
                                                 "A staff member will be with you shortly. Please explain your issue and include all relevant information.")
                await message.author.send(embed=embed)

                embed = await utils.create_embed(f"Ticket Opened by {message.author.name}#{message.author.discriminator}",
                                                 f"This ticket has been opened by {message.author.mention}")
                welcome_message = await user_support_channel.send(embed=embed, view=CloseButton(self.bot))
                await welcome_message.pin()
                await user_support_channel.purge(limit=1)
            if str(message.attachments) != "[]":
                sent_attachment = await message.attachments[0].to_file(use_cached=False, spoiler=False)
                await user_support_channel.send(content=message.content, file=sent_attachment)
            else:
                await user_support_channel.send(message.content)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if isinstance(after.author, discord.ClientUser) or self.bot.get_guild(config.gateway_guild_id) in after.author.mutual_guilds:
            return
        if isinstance(after.channel, discord.channel.DMChannel) and not before.content.startswith(config.prefix) and before.content != after.content:
            ticket_channel: discord.TextChannel = discord.utils.get(self.bot.get_guild(config.guild_id).text_channels, name=f"ticket-{after.author.id}")
            embed = await utils.create_embed("Message edited",
                                             f"{after.author.mention} has edited their message.")
            embed.add_field(name="Before", value=before.content)
            embed.add_field(name="After", value=after.content)
            await ticket_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
