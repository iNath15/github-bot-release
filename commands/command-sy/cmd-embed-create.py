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

    # Prompt the user to enter the name of the command and image folder
    await message.channel.send('What would you like to name this embed command?')

    # Wait for the user's response, with a timeout of 30 seconds
    try:
        response = await asyncio.wait_for(client.wait_for('message', check=lambda m: m.author == message.author), timeout=30)
    except asyncio.TimeoutError:
        # If the user doesn't respond within the timeout, send a message and return
        await message.channel.send('Timed out waiting for response.')
        return

    command_name = response.content.strip().lower()

    # Read the code from the text file
    with open('code-embed.txt', 'r') as f:
        code = f.read()

    # Replace the placeholder with the actual command name
    code = code.replace('(name of folder created)', command_name)

    # Create the command file
    command_file_path = f'commands/command-usr/{command_name}.py'
    if os.path.exists(command_file_path):
        await message.channel.send(f'The command {command_name} already exists.')
        return
    with open(command_file_path, 'w') as f:
        f.write(code)

    # Create the image folder
    image_folder_path = f'commands/images/{command_name}'
    os.makedirs(image_folder_path, exist_ok=True)

    # Create the color folder
    color_folder_path = f'commands/color/{command_name}'
    os.makedirs(color_folder_path, exist_ok=True)


    

    # Create the text folder
    text_folder_path = f'commands/text/{command_name}'
    os.makedirs(text_folder_path, exist_ok=True)


    await message.channel.send(f'The command {command_name} has been created')