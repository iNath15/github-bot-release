# type: ignore
import discord
from discord import Activity, ActivityType
import config
import asyncio

async def run(client, message, user_ping, args):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send('What type of status would you like? \n**0**: Default Status \n**1**: Playing Game \n**2**: Streaming \n**3**: Listening \n**4**: Watching')

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await client.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    status_type = response.content
    
    await message.channel.send('What would you like the status to be?')

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await client.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    status = response.content

    status_url = None

    if status_type == 2:
        await message.channel.send("What URL would you like to use for the stream?")

        # Wait for the user's response
        def check(m):
            return m.channel == message.channel and m.author == message.author
        try:
            response = await client.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await message.channel.send("You didn't respond in time.")
            return

        status_url = response.content

    if status_type == 1:
        game = discord.Game(f'{status}')
        await client.change_presence(activity=game)
    elif status_type == 2:
        stream = discord.Streaming(name=status, url=f'{status_url}')
        await client.change_presence(activity=stream)
    elif status_type == 3:
        listen = discord.Activity(type=discord.ActivityType.listening, name=status)
        await client.change_presence(activity=listen)
    elif status_type == 4:
        watch = discord.Activity(type=discord.ActivityType.watching, name=status)
        await client.change_presence(activity=watch)
    else:
        listen = discord.Activity(type=discord.ActivityType.listening, name="Chikatto Chika Chika")
        await client.change_presence(activity=listen)


    # Read the contents of the config.py file
    with open('config.py', 'r') as f:
        config_contents = f.read()

    # Replace the values in the config
    config_contents_type = config_contents.replace(f'STATUS_TYPE = {config.STATUS_TYPE}', f'STATUS_TYPE = {status_type}')
    config_contents_status = config_contents.replace(f'STATUS = {config.STATUS}', f'STATUS = {status}')
    config_contents_url = config_contents.replace(f'STATUS_URL = {config.STATUS_URL}', f'STATUS_URL = {status_url}')

    # Write the modified contents back to the config.py file
    with open('config.py', 'w') as f:
        f.write(config_contents_type)
        f.write(config_contents_status)
        f.write(config_contents_url)

    # Update the variables in the config module
    config.STATUS_TYPE = status_type
    config.STATUS = status
    config.STATUS_URL = status_url

    # Send a message confirming the change
    await message.channel.send(f"Status successfully changed to {status}")
