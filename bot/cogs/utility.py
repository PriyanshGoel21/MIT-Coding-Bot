import sys
import time
from datetime import datetime

import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now().replace(microsecond=0)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{type(self).__name__} Cog ready.")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!")
        before_time = time.time()
        msg = await ctx.send(embed=embed)
        latency = round(self.bot.latency * 1000)
        elapsed_ms = round((time.time() - before_time) * 1000) - latency
        embed.add_field(name="Ping", value=f"{elapsed_ms}ms")
        embed.add_field(name="Latency", value=f"{latency}ms")
        await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
