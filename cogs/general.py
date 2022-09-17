import time

import discord
from discord.ext import commands

from utillities import bot_has_permissions
from utillities.discordbot import DiscordBot


class General(commands.Cog, name="general"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel.id == 1020124128486883398 and message.embeds:
            await message.channel.send("<@&1020327962865844385>", embeds=message.embeds)
            await message.delete()

    @bot_has_permissions(send_messages=True)
    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        """Show latency in seconds & milliseconds"""

        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f":ping_pong: Pong! in {int(ping)}ms")


async def setup(bot: DiscordBot):
    await bot.add_cog(General(bot))
