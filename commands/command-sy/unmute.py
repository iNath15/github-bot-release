# type: ignore
import discord
import config

async def run(client, message, args, user_ping):
    has_permission = False
    for role in message.author.roles:
        if role.permissions.mute_members:
            has_permission = True
            break
    if not has_permission:
        await message.channel.send("You do not have permission to use this command.")
        return
    # Get the mention of the user to unmute
    user_to_unmute = message.mentions[0]
    # Get the mute role
    mute_role = discord.utils.get(message.guild.roles, id=config.MUTE_ROLE)
    # Check if the user is not in the mute role
    if mute_role not in user_to_unmute.roles:
        await message.channel.send(f"{user_to_unmute.mention} is not muted.")
        return
    # Remove the user from the mute role
    await user_to_unmute.remove_roles(mute_role)
    await message.channel.send(f"{user_to_unmute.mention} has been unmuted.")