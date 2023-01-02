import asyncio
import os
import aiohttp
from constants import TOKEN

import hikari
import lightbulb
import miru

intents = hikari.Intents.ALL

bot = lightbulb.BotApp(
    token=TOKEN,
    intents=intents,
    prefix="-",
    banner=None,
    default_enabled_guilds=[856636948667301908]
)

@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! {bot.heartbeat_latency*1000:.2f}")


miru.install(bot)

bot.load_extensions_from("./extensions")


@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

if __name__ == "__main__":
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    bot.run()