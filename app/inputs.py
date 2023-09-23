async def take_user_input(ctx, bot_messages, messages_to_delete):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    user_responses = {}

    for response_key, bot_message in bot_messages.items():
        bot_msg = await ctx.send(bot_message)

        messages_to_delete.append(bot_msg)

        user_msg = await ctx.bot.wait_for("message", check=check, timeout=60)
        user_response = user_msg.content
        messages_to_delete.append(user_msg)

        user_responses[response_key] = user_response

    return user_responses
