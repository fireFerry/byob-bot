import os
import discord.ext
import asyncio
import sqlite3
from discord.ext import commands
from config import config
import cogs.utils as utils

bot = commands.Bot(command_prefix=config.prefix, help_command=None, intents=discord.Intents.all())


async def start_bot():
    for filename in os.listdir("./cogs"):  # load all cogs
        if filename.endswith(".py") and filename != "__init__.py" and filename != "utils.py" and filename != "prints.py":
            await bot.load_extension(f'cogs.{filename[:-3]}')
    if config.debug:
        await bot.load_extension("cogs.prints")
    if not os.path.exists("tickets.db"):  # create database if it doesn't exist
        conn = sqlite3.connect("tickets.db")
        conn.cursor().execute("CREATE TABLE tickets (member_id INT, thread_id INT)")
        conn.commit()
        conn.close()
    if not os.path.exists("config/autorole.json"):  # create autorole.json if it doesn't exist
        with open("config/autorole.json", 'w') as f:
            f.write("{}")
            f.close()
    if not os.path.exists("config/reactionroles.json"):  # create reactionroles.json if it doesn't exist
        with open("config/reactionroles.json", 'w') as f:
            f.write("{}")
            f.close()

asyncio.run(start_bot())


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if config.debug:
        raise error
    if isinstance(error, commands.CommandNotFound):  # ignore command not found errors
        return
    if isinstance(error, commands.CheckFailure):  # Send message when user has insufficient permissions
        await utils.send_embed("Error",
                               "You do not have permission to do this.",
                               ctx,)
        return
    raise error


bot.run(config.token)
