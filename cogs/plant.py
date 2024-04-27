""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

from discord.ext import commands
from discord.ext.commands import Context

import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
class Plant(commands.Cog, name="Plant"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(
        name="ledon",
        description="Turn on the LED.",
    )
    async def ledon(self, context: Context) -> None:
        res = await fetch_data("http://192.168.1.110/api/v1/led?color=1")
        await context.send(res)
        
    @commands.hybrid_command(
        name="ledoff",
        description="Turn off the LED.",
    )
    async def ledoff(self, context: Context) -> None:
        res = await fetch_data("http://192.168.1.110/api/v1/led?color=0")
        await context.send(res)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Plant(bot))