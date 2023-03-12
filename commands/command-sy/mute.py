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
    # Get the mention of the user to mute
    user_to_mute = message.mentions[0]
    # Get the mute role
    mute_role = discord.utils.get(message.guild.roles, id=config.MUTE_ROLE)
    # Check if the mute role is not set
    if mute_role is None:
        print(f'Mute role id: {config.MUTE_ROLE}')
        await message.channel.send(f'No mute role has been set. you can add one with ``{config.PREFIX} mute-set``')
        return
    # Check if the user is already in the mute role
    if mute_role in user_to_mute.roles:
        await message.channel.send(f"{user_to_mute.mention} is already muted.")
        return
    # Add the user to the mute role
    await user_to_mute.add_roles(mute_role)
    await message.channel.send(f"{user_to_mute.mention} has been muted.")
    