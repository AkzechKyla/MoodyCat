import settings
import discord

import asyncio


from discord.ext import commands

from datetime import datetime, timedelta


logger = settings.logging.getLogger("bot")


def main():
    intents = discord.Intents.default()

    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.event
    async def on_message(message: discord.Message) -> None:
        await bot.process_commands(message)

        asyncio.create_task(stick_message(message))

    async def take_user_input(ctx, bot_messages, messages_to_delete):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        user_responses = {}

        for response_key, bot_message in bot_messages.items():
            bot_msg = await ctx.send(bot_message)

            messages_to_delete.append(bot_msg)

            user_msg = await bot.wait_for("message", check=check, timeout=60)
            user_response = user_msg.content
            messages_to_delete.append(user_msg)

            user_responses[response_key] = user_response

        return user_responses

    async def parse_sleep(sleep_time, wake_time):
        try:
            sleep_time_obj = datetime.strptime(sleep_time, "%I:%M %p")

            wake_time_obj = datetime.strptime(wake_time, "%I:%M %p")

            if sleep_time_obj > wake_time_obj:
                wake_time_obj += timedelta(days=1)

            total_hours = (wake_time_obj - sleep_time_obj).total_seconds() / 3600

        except ValueError:
            return "Invalid time format. Please use the format 'hh:mm AM/PM'."

        return total_hours

    async def delete_messages(ctx, messages_to_delete):
        for message in messages_to_delete:
            asyncio.create_task(message.delete())

        asyncio.create_task(ctx.message.delete())

    @bot.command(
        help="Converts your sleep time in 12-hour time format into total hours to track how long you've slept for the day.",
        description="Command Info:",
        brief="Tracks how long you've slept",
    )
    async def sleephours(ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        bot_messages = {
            "date_sleep": "**What date did you last sleep?** (Enter in dd/mm/yyyy format, e.g., 15/09/2023)",
            "sleep_time": "**When exactly did you last sleep?** (Enter in 12-hour time format, e.g., 12:00 AM)",
            "wake_time": "**When exactly did you last wake up?** (Enter in 12-hour time format, e.g., 8:00 AM)",
        }

        messages_to_delete = []

        try:
            user_responses = await take_user_input(
                ctx, bot_messages, messages_to_delete
            )

            date_sleep = user_responses["date_sleep"]

            sleep_time = user_responses["sleep_time"]

            wake_time = user_responses["wake_time"]

            total_hours = await parse_sleep(sleep_time, wake_time)

            await ctx.send(
                f"```"
                f"DATE: {date_sleep}"
                f"```\n"
                f"<@{ctx.author.id}>'s **SLEEP HOURS:**\n"
                f"> {sleep_time} - {wake_time} ({total_hours:.2f} hours)"
            )

            await delete_messages(ctx, messages_to_delete)

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the information. Command canceled."
            )

    @bot.command(
        help="Adds additional sleep information to your previous record.",
        description="Command Info:",
        brief="Adds additional sleep info",
    )
    async def addsleep(
        ctx,
        msg_id: int = None,
        channel: discord.TextChannel = None,
    ):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        channel = channel or ctx.channel

        try:
            if not msg_id:
                await ctx.send("You have not provided a message id.")

            sleep_msg = await channel.fetch_message(msg_id)

            bot_messages = {
                "sleep_time": "**When exactly did you last sleep?** (Enter in 12-hour time format, e.g., 12:00 AM)",
                "wake_time": "**When exactly did you last wake up?** (Enter in 12-hour time format, e.g., 8:00 AM)",
            }

            messages_to_delete: list[str] = []

            user_responses = await take_user_input(
                ctx, bot_messages, messages_to_delete
            )

            sleep_time = user_responses["sleep_time"]

            wake_time = user_responses["wake_time"]

            total_hours = await parse_sleep(sleep_time, wake_time)

            new_content = f"> {sleep_time} - {wake_time} ({total_hours:.2f} hours)"

            await sleep_msg.edit(content=sleep_msg.content + "\n" + new_content)

            await delete_messages(ctx, messages_to_delete)

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the information. Command canceled."
            )

    @bot.command(
        help="help info.",
        description="Command Info:",
        brief="brief help info",
    )
    async def stick_message(message: discord.Message) -> None:
        if message.channel.id != 1028932255256682536:  # sorcery-lab
            return
        if message.author.id == bot.user.id:
            return

        total_score = 100

        prefix = "\u200c"
        c = f"Your score for today is **{total_score}**!"
        c = f"{prefix}{c}"

        async for m in message.channel.history(limit=5):
            if m.author.id == bot.user.id:
                if m.content.startswith(prefix):
                    asyncio.create_task(m.delete())
                    asyncio.create_task(m.channel.send(c))
                    break
        else:
            await m.channel.send(c)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    main()
