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
    await message.channel.send('Which command do you want to add text to?')

    # Wait for the user's response, with a timeout of 30 seconds
    try:
        response = await asyncio.wait_for(bot.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    command_name = response.content.strip().lower()

    # Check if the command exists
    text_folder_path = f'commands/text/{command_name}'
    if not os.path.exists(text_folder_path):
        await message.channel.send(f'Command {command_name} not found')
        return

    # Ask the user for the contents of the text file
    await message.channel.send('Enter the contents of the text file:')
    try:
        file_contents_response = await asyncio.wait_for(bot.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    # Extract the message content from the response message
    file_contents = file_contents_response.content

    # Find the next available file name
    i = 1
    while True:
        file_name = f"{text_folder_path}/{i}.txt"
        if not os.path.exists(file_name):
            break
        i += 1

    # Write the contents to the file
    with open(file_name, "w") as f:
        f.write(file_contents)

    # Reply to the user
    await message.channel.send(f'Your embed title has been added')
