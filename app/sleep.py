from datetime import datetime, timedelta
import discord


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


async def sleepinfo_embed(description, title, embed_footer):
    embed = discord.Embed(
        colour=discord.Colour.dark_blue(),
        description=f"{description}",
        title=f"{title}",
    )

    embed.set_footer(text=f"{embed_footer}")
    embed.set_author(name="💤SLEEP HOURS💤")

    return embed
