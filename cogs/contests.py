import datetime
import os
import time

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

    @tasks.loop(hours=24)
    async def update_contests(self):
        headers = {"Authorization": os.getenv("CLIST_API_KEY")}
        guild: discord.Guild = self.bot.get_guild(1001523934979690566)
        channel: discord.TextChannel = guild.get_channel(1020124128486883398)
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
                                    guild.scheduled_events, name=obj["event"]
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
                                        ).astimezone(tz=datetime.timezone.utc),
                                        end_time=datetime.datetime.strptime(
                                            obj["end"], "%Y-%m-%dT%H:%M:%S"
                                        ).astimezone(tz=datetime.timezone.utc),
                                        location=obj["href"],
                                    )
                                    await channel.send(
                                        f"<@&1020327962865844385>\n{event.url}"
                                    )
                                except Exception as E:
                                    print(E)
                except Exception as E:
                    print(E)


async def setup(bot: DiscordBot):
    await bot.add_cog(Contests(bot))
