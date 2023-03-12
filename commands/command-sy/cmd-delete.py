# type: ignore
import os
import asyncio
import shutil

async def run(client, message, user_ping, args):
        
    # Only process commands from members (not bots)
    if message.author.bot:
        return

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    command_folders = os.listdir('commands/images')

    if not command_folders:
        await message.channel.send("There are no commands to delete.")
        return

    await message.channel.send("Which command do you want to delete? Type the name of the command or type `cancel` to cancel the command.")

    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        command_name = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await message.channel.send("Timed out waiting for user response.")
        return
    command_name = command_name.content.lower()

    if command_name == "cancel":
        await message.channel.send("Deletion cancelled.")
        return

    if command_name not in command_folders:
        await message.channel.send("The selected command does not exist.")
        return

    await message.channel.send(f"Are you sure you want to delete the `{command_name}` command? Type `confirm {command_name}` to confirm or type `cancel` to cancel the deletion.")

    try:
        confirm = await client.wait_for('message', check=check, timeout=60.0)
    except asyncio.TimeoutError:
        await message.channel.send("Timed out waiting for user response.")
        return
    confirm = confirm.content.lower()

    if confirm == "cancel":
        await message.channel.send("Command cancelled.")
        return

    if confirm != f"confirm {command_name}":
        await message.channel.send("Incorrect confirmation. Deletion cancelled.")
        return

    # Delete the command folders
    if os.path.exists(f"commands/command-usr/{command_name}.py"):
        os.remove(f"commands/command-usr/{command_name}.py")

    if os.path.exists(f"commands/images/{command_name}"):
        shutil.rmtree(f"commands/images/{command_name}")

    if os.path.exists(f"commands/text/{command_name}"):
        shutil.rmtree(f"commands/text/{command_name}")

    if os.path.exists(f"commands/color/{command_name}"):
        shutil.rmtree(f"commands/color/{command_name}")


    await message.channel.send(f"The `{command_name}` command has been deleted.")