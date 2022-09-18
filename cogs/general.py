import time

import discord
from discord.ext import commands

from utillities import bot_has_permissions
from utillities.discordbot import DiscordBot
from views.reaction_roles import CompetitiveCoding, LanguageRoles


class General(commands.Cog, name="general"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ...

    @commands.is_owner()
    @commands.command()
    async def test(self, ctx: commands.Context):
        channel = ctx.guild.get_channel(1019262719662247967)
        await channel.purge()
        try:
            await channel.send(
                embed=discord.Embed(
                    title="Competitive Coding",
                    description=f"Click the button below to get <@&1020327962865844385> role\n\nNote: Check for ongoing competitions in <#1020948698492043314> or events regularly.",
                    colour=discord.Colour.random(),
                ),
                view=CompetitiveCoding(),
            )
            await channel.send(
                embed=discord.Embed(
                    title="Language Roles",
                    description=f"Click the button(s) below to get language roles",
                    colour=discord.Colour.random(),
                ),
                view=LanguageRoles(),
            )
        except Exception as E:
            print(E)

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
