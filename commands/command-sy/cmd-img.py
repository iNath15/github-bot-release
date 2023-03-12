# type: ignore
import os
import asyncio


async def run(client, message, user_ping, args):
    # Only process commands from members (not bots)
    if message.author.bot:
        return

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    # Prompt the user to enter the name of the command
    await message.channel.send('Which command would you like to add images to?')

    # Wait for the user's response, with a timeout of 30 seconds
    try:
        response = await asyncio.wait_for(client.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    command_name = response.content.strip().lower()

    # Check if the command exists
    command_file_path = f'commands/command-usr/{command_name}.py'
    if not os.path.exists(command_file_path):
        await message.channel.send(f'Invalid command: {command_name}')
        return

    # Prompt the user to upload the images
    await message.channel.send('Upload the images you wish to add')

    # Wait for the user to upload the images
    def check(m):
        return m.author == message.author and m.attachments

    try:
        response = await asyncio.wait_for(client.wait_for('message', check=check), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    attachments = response.attachments

    # Download the images and save them to the image folder
    image_folder_path = f'commands/images/{command_name}'
    for attachment in attachments:
        file_path = os.path.join(image_folder_path, attachment.filename)
        await attachment.save(file_path)

    # Confirm the action has been completed
    await message.channel.send(f'Images have been added to the command {command_name}')