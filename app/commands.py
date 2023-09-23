import asyncio
import discord
from app.inputs import take_user_input
from app.messages import delete_messages
from app.sleep import parse_sleep, sleepinfo_embed


def setup_commands(bot):
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

            sleep_info = f"{sleep_time} - {wake_time} ({total_hours:.2f} hours)"
            embed_footer = f"created by {ctx.author}"

            embed = await sleepinfo_embed(sleep_info, date_sleep, embed_footer)

            await ctx.send(embed=embed)

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
        msg_id: int | None = None,
        channel: discord.TextChannel | None = None,
    ):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        channel = channel or ctx.channel

        try:
            if msg_id is None:
                await ctx.send("You have not provided a message id.")
                return

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

            existing_embed_description = sleep_msg.embeds[0].description
            existing_embed_title = sleep_msg.embeds[0].title
            embed_footer = f"created by {ctx.author}"

            new_description = f"{existing_embed_description}\n{sleep_time} - {wake_time} ({total_hours:.2f} hours)"

            updated_embed = await sleepinfo_embed(
                new_description, existing_embed_title, embed_footer
            )

            await sleep_msg.edit(embed=updated_embed)
            await delete_messages(ctx, messages_to_delete)

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the information. Command canceled."
            )

    @bot.command()
    async def addaction(ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        bot_messages = {
            "action": "**Enter an action you want to add on your list of actions**",
            "points": "**Enter corresponding points for that action, e.g., +2 or -1**",
        }

        messages_to_delete = []

        try:
            user_responses = await take_user_input(
                ctx, bot_messages, messages_to_delete
            )

            action = user_responses["action"]
            points = user_responses["points"]

            await ctx.send(f'"**{action}**" with **{points} points** is added!')

            await delete_messages(ctx, messages_to_delete)

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to provide the information. Command canceled."
            )
