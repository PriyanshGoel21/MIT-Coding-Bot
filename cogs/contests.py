import datetime
import os
import time
from zoneinfo import ZoneInfo

import aiohttp
import discord
from discord.ext import commands, tasks

from utillities import bot_has_permissions
from utillities.discordbot import DiscordBot


class Contests(commands.Cog, name="contests"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.update_contests.start()
        self.reminder.start()

    @tasks.loop(minutes=1)
    async def reminder(self):
        guild: discord.Guild = self.bot.get_guild(1001523934979690566)
        channel: discord.TextChannel = guild.get_channel(1020948698492043314)
        now = discord.utils.utcnow()
        for event in guild.scheduled_events:
            if (event.start_time - now).total_seconds() // 60 == 60:
                await channel.send(
                    f"<@&1020327962865844385> EVENT STARTING IN 1 HOUR\n\n{event.url}"
                )

    @tasks.loop(hours=24)
    async def update_contests(self):
        headers = {"Authorization": os.getenv("CLIST_API_KEY")}
        guild: discord.Guild = self.bot.get_guild(1001523934979690566)
        channel: discord.TextChannel = guild.get_channel(1020948698492043314)
        async with aiohttp.ClientSession() as session:
            resource_ids = [
                1,  # codeforces
                2,  # codechef
                12,  # topcoder
                102,  # leetcode
                35,  # google
            ]
            for resource_id in resource_ids:
                try:
                    async with session.get(
                        f"https://clist.by/api/v2/contest/?upcoming=true&order_by=start&resource_id={resource_id}",
                        headers=headers,
                    ) as response:
                        data = await response.json()
                        for obj in data["objects"]:
                            if (
                                discord.utils.get(
                                    guild.scheduled_events,
                                    location=obj["href"],
                                )
                                is None
                            ):
                                try:
                                    event: discord.ScheduledEvent = await guild.create_scheduled_event(
                                        name=obj["event"],
                                        description=f"{obj['event']}\n\n{obj['href']}",
                                        start_time=datetime.datetime.strptime(
                                            obj["start"],
                                            "%Y-%m-%dT%H:%M:%S",
                                        ).replace(tzinfo=datetime.timezone.utc),
                                        end_time=datetime.datetime.strptime(
                                            obj["end"], "%Y-%m-%dT%H:%M:%S"
                                        ).replace(tzinfo=datetime.timezone.utc),
                                        location=obj["href"],
                                    )
                                    await channel.send(
                                        f"NEW EVENT ADDED\n\n{event.url}",
                                    )
                                except Exception as E:
                                    print(E)
                except Exception as E:
                    print(E)

    @commands.is_owner()
    @commands.command()
    async def update_events(self, ctx: commands.Context):
        await ctx.message.delete()
        for event in ctx.guild.scheduled_events:
            await event.delete()
        await self.update_contests()


async def setup(bot: DiscordBot):
    await bot.add_cog(Contests(bot))
