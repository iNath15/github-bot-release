# type: ignore
import os
import asyncio

async def run(bot, message, user_ping, args):

    # Only process commands from members (not bots)
    if message.author.bot:
        return

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    # Prompt the user to enter the name of the command
    await message.channel.send('Which command do you want to add color to?')

    # Wait for the user's response, with a timeout of 30 seconds
    try:
        response = await asyncio.wait_for(bot.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    command_name = response.content.strip().lower()

    # Check if the command exists
    color_folder_path = f'commands/color/{command_name}'
    if not os.path.exists(color_folder_path):
        await message.channel.send(f'Command {command_name} not found')
        return

    # Ask the user for the hex code
    await message.channel.send('Enter the hex code for the color:')
    try:
        hex_code_response = await asyncio.wait_for(bot.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    # Extract the message content from the response message
    hex_code = hex_code_response.content

    # Find the file name
    file_name = f"{color_folder_path}/color.txt"

    # Write the hex code to the file
    with open(file_name, "w") as f:
        f.write(hex_code)

    # Reply to the user
    await message.channel.send(f'Your embed has been given a new color')