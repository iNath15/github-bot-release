async def run(bot, message, args, user_ping):
    guild = message.guild
    member_count = len(guild.members)
    bot_count = sum(1 for member in guild.members if member.bot)
    human_member_count = member_count - bot_count
    await message.channel.send(f"There's a total of **{member_count}** members!\n**{human_member_count}** people, and **{bot_count}** bots")