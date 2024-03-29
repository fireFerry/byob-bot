import discord.ext
import os
from discord.ext import commands
from config import config
import cogs.utils as utils


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # shutdown command, only usable by the owner.

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        await self.bot.change_presence(status=discord.Status.invisible)
        await utils.send_embed("Shutdown",
                               f"{self.bot.user} has been shut down.",
                               ctx,)
        await self.bot.close()
        print(f'{self.bot.user.name} has been shut down.')

    # reboot command, only usable by the owner.

    @commands.command()
    @commands.is_owner()
    async def reboot(self, ctx: commands.Context):
        await self.bot.change_presence(status=discord.Status.invisible)
        await utils.send_embed("Rebooting",
                               "Reboot initiated.",
                               ctx,)
        print(f'{self.bot.user} is rebooting...')
        os.system('sh update.sh')

    # dev-status command, only usable by the owner.

    @commands.command()
    @commands.is_owner()
    async def dev_status(self, ctx: commands.Context):
        autorolestatus, _ = await utils.autorole_status(ctx.guild.id)
        embed = await utils.create_embed("Dev Status",
                                         f"**Status**: Running version {config.byob_bot_version}.\n**Ping**: {round(self.bot.latency * 1000)}ms\n**Prefix**: {config.prefix}\n**Autorole status**: {autorolestatus}",
                                         )
        embed.add_field(name="**Server stats**",
                        value=f"**Name**: {ctx.guild.name}\n**Members**: {ctx.guild.member_count}\n**Description**: {ctx.guild.description}",
                        inline=False)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        await self.bot.reload_extension(f"cogs.{extension}")
        await utils.send_embed("Extension reloaded",
                               f"{extension} has been reloaded.",
                               ctx,)

    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx: commands.Context, extension: str):
        await self.bot.unload_extension(f'cogs.{extension}')
        await utils.send_embed("Extension Disabled",
                               f"{extension} has been disabled.",
                               ctx,)

    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx: commands.Context, extension: str):
        await self.bot.load_extension(f'cogs.{extension}')
        await utils.send_embed("Extension Enabled",
                               f"{extension} has been enabled.",
                               ctx,)


async def setup(bot):
    await bot.add_cog(Owner(bot))
