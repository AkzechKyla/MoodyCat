import asyncio
import discord


async def delete_messages(ctx, messages_to_delete):
    for message in messages_to_delete:
        asyncio.create_task(message.delete())

    asyncio.create_task(ctx.message.delete())


async def stick_message(bot, message: discord.Message) -> None:
    if message.channel.id != 1028932255256682536:  # sorcery-lab
        return

    if bot is None or bot.user is None:
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
