async def run(client, message, user_ping, args):
    # Check if the user has the necessary permissions
    if not message.author.guild_permissions.ban_members:
        await message.channel.send("You do not have permission to Ban others")
        return

    # Check if the user provided a user to ban
    if not message.mentions:
        await message.channel.send("You must mention a user to Ban.")
        return

    # Get the user to Ban
    user_to_ban = message.mentions[0]

    # Get the reason for the Ban (if provided)
    reason = args.strip() if args else "No reason provided"

    # Ban the user and send a message to confirm the Ban
    await message.guild.ban(user_to_ban, reason=reason)
    await message.channel.send(f"{user_to_ban.name} has been Banned.")
