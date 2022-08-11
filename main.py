import os
import discord.ext
import asyncio
from discord.ext import commands
from config import config
import cogs.utils as utils

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.prefix, help_command=None, intents=intents)


async def start_bot():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py" and filename != "utils.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')

asyncio.run(start_bot())


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        await utils.send_embed("Error",
                               "You do not have permission to do this.",
                               ctx,)
        return
    raise error


bot.run(config.token)
