import os
from pathlib import Path

from bot import utils
from discord.ext import commands


bot = commands.AutoShardedBot(command_prefix=utils.config.prefix)


@bot.event
async def on_ready():
    print("Ready")


def extensions():
    files = Path("bot", "cogs").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(_bot):
    for ext in extensions():
        try:
            _bot.load_extension(ext)
        except Exception as ex:
            print(f"Failed to  load extension {ext} - exception: {ex}")


def run():
    load_extensions(bot)
    bot.run(utils.config.token)
