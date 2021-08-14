import os
import discord.ext
from discord.ext import commands
from config import config
from dotenv import load_dotenv
from discord.ext.commands import CommandNotFound

#load_dotenv()
#intents = discord.Intents.default()
#intents.members = True

client = commands.Bot(command_prefix=config.prefix)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        client.load_extension(f'cogs.{filename[:-3]}')

async def on_command_error(ctx, error):

        send_help = (
        commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)

        if isinstance(error, commands.CommandNotFound):  # fails silently
            pass

        elif isinstance(error, send_help):
            _help = await send_cmd_help(ctx)
            await ctx.send(embed=_help)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command.')
        # If any other error occurs, prints to console.
        else:
            print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))






client.run(config.token)