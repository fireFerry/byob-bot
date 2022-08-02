import discord
import chat_exporter
import asyncio
import io
from discord.ext import commands
from config import config
import cogs.utils as utils


class CloseButton(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", custom_id="close", style=discord.ButtonStyle.red)
    async def close_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = await self.bot.get_context(interaction.message)
        send_member = await commands.MemberConverter().convert(ctx, ctx.channel.name.split("-")[1])
        embed = await utils.create_embed("Ticket Closed",
                                         "A staff member has closed your ticket. Sending a new message will create a new ticket, please only do so if you have a new issue.",
                                         )
        if not send_member.dm_channel:
            await send_member.create_dm()
        await send_member.dm_channel.send(embed=embed)
        embed = await utils.create_embed("Ticket Closed",
                                         "Ticket will be deleted in 5 seconds...",
                                         )
        button.label = "Closed"
        button.disabled = True
        await interaction.response.send_message(embed=embed, view=self)
        transcript = await chat_exporter.export(ctx.channel, military_time=True)
        if transcript is None:
            return
        transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                       filename=f"transcript-{ctx.channel.name}.html")
        transcript_channel: discord.TextChannel = discord.utils.get(ctx.guild.text_channels,
                                                                    name="ticket-transcripts")
        embed = await utils.create_embed()
        embed.set_author(name=f"{send_member.name}#{send_member.discriminator}",
                         icon_url=f"{send_member.avatar.url}")
        embed.add_field(name="**Ticket Owner**", value=f"{send_member.mention}", inline=True)
        embed.add_field(name="**Ticket Owner ID**", value=f"{send_member.id}", inline=True)
        embed.add_field(name="**Ticket Name**", value=f"{ctx.channel.name}", inline=True)
        await transcript_channel.send(embed=embed, file=transcript_file)
        await asyncio.sleep(5)
        await interaction.channel.delete(reason="Ticket closed.")
        self.stop()


class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CloseButton(self.bot))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if hasattr(message.channel, 'category') and str(message.channel.category) == "Active Tickets":
            if message.guild.id != config.guild_id or message.content == f"{config.prefix}close":
                return
            send_member = await commands.MemberConverter().convert(await self.bot.get_context(message), message.channel.name.split("-")[1])
            if not send_member.dm_channel:
                await send_member.create_dm()
            if str(message.attachments) != "[]":
                sent_attachment = await message.attachments[0].to_file(use_cached=False, spoiler=False)
                await send_member.dm_channel.send(content=message.content, file=sent_attachment)
            else:
                await send_member.dm_channel.send(message.content)
        if isinstance(message.channel, discord.channel.DMChannel):
            if message.content.startswith(config.prefix):
                await self.bot.process_commands(message)
                return
            support_server = self.bot.get_guild(config.guild_id)
            member = await support_server.fetch_member(message.author.id)
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


async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
