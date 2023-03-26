import config
import asyncio
import re

async def run(bot, message, user_ping, args):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send("Please mention the channel you want to set as the welcome channel.")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await bot.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    # Extract the channel ID from the user's response
    channel_match = re.match(r"<#(\d+)>", response.content)
    if not channel_match:
        await message.channel.send("You didn't mention a valid channel.")
        return
    channel_id = channel_match.group(1)

    # Read the contents of the config.py file
    with open('config.py', 'r') as f:
        config_contents = f.read()

    # Replace the value of the Channel variable with the new Channel
    config_contents = config_contents.replace(f'WELCOME_CHL = {config.WELCOME_CHL}', f'WELCOME_CHL = {channel_id}')

    # Write the modified contents back to the config.py file
    with open('config.py', 'w') as f:
        f.write(config_contents)

    # Update the WELCOME_CHL variable in the config module
    config.WELCOME_CHL = channel_id

    # Send a message confirming the change
    await message.channel.send(f"Welcome channel successfully set to <#{channel_id}>")
