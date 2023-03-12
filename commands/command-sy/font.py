import os
import asyncio
from config import FONT  # Import the FONT variable from config.py
import config

async def run(client, message, user_ping, args):
    # Only process commands from members (not bots)
    if message.author.bot:
        return

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    # Prompt the user to enter the name of the command
    await message.channel.send('Please upload the font you want to use.\n(.ttf and .otf filetypes are supported)')

    # Wait for the user to upload the font file
    def check(m):
        return m.author == message.author and m.attachments

    try:
        response = await asyncio.wait_for(client.wait_for('message', check=check), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    attachments = response.attachments

    # Download the font file and save it to the font folder
    font_path = 'font'  # Remove the leading forward slash
    for attachment in attachments:
        if attachment.filename.endswith('.ttf') or attachment.filename.endswith('.otf'):
            # Delete the existing font file
            os.remove(os.path.join(font_path, FONT))

            # Save the new font file
            file_path = os.path.join(font_path, attachment.filename)
            await attachment.save(file_path)

            # Update the FONT variable in config.py
            with open('config.py', 'r') as f:
                config_lines = f.readlines()

            for i in range(len(config_lines)):
                if config_lines[i].startswith('FONT'):
                    config_lines[i] = f'FONT = "{attachment.filename}"\n'
                    break

            with open('config.py', 'w') as f:
                f.writelines(config_lines)

            config.FONT = f'{attachment.filename}'

            # Confirm the action has been completed
            await message.channel.send(f'The font has been updated to {attachment.filename}.')
            return
        else:
            await message.channel.send('Invalid file type. Please upload a .ttf or .otf file.')
            return
