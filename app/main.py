import asyncio
import discord
from discord.ext import commands
from app import settings
from app.messages import stick_message
from app.commands import setup_commands

logger = settings.logging.getLogger("bot")
_bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

setup_commands(_bot)


@_bot.event
async def on_ready():
    logger.info(f"User: {_bot.user} (ID: {_bot.user.id})")


@_bot.event
async def on_message(message: discord.Message) -> None:
    await _bot.process_commands(message)

    asyncio.create_task(stick_message(_bot, message))


def main():
    _bot.run(settings.DISCORD_API_SECRET, root_logger=True)
