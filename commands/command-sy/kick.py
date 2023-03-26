async def run(bot, message, user_ping, args):
    # Check i fthe  user has the necessary permissions
    if not message.author.guild_permissions.kick_members:
        await message.channel.send("You do not have permission to Kick others")
        return

    # Check if the user privided a user to kick
    if not message.mentions:
        await message.channel.send("You must mention a user to Kick")
        return

    # Get the user to Kick
    user_to_kick = message.mentions[0]

    # Get the reason for the Kick (if provided)
    reason = args.strip() if args else "No reason provided"

    # Kick the user and send a message to confirm the Kick
    await message.guild.kick(user_to_kick, reason=reason)
    await message.channel.send(f"{user_to_kick.name} has been Kicked")