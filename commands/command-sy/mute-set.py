# type: ignore
import config
import re
import importlib

async def run(client, message, user_ping, args):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send("Which role would you like to set as mute?")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await client.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    # Set the prefix to the user's response
    role = response.content
    new_mute = re.sub('[<@&>]', '', role)

    # Read the contents of the config.py file
    with open('config.py', 'r') as f:
        config_contents = f.read()

    # Set the MUTE_ROLE to an empty string if it is not already defined
    if 'MUTE_ROLE' not in config_contents:
        config_contents += '\nMUTE_ROLE = '

    # Replace the value of the MUTE_ROLE variable with the new mute role
    config_contents = config_contents.replace(f'MUTE_ROLE = {config.MUTE_ROLE}', f'MUTE_ROLE = {new_mute}')

    # Write the modified contents back to the config.py file
    with open('config.py', 'w') as f:
        f.write(config_contents)

    # Update the MUTE_ROLE variable in the config module
    config.MUTE_ROLE = new_mute

    # Reload the config module
    importlib.reload(config)

    # Send a message confirming the change
    await message.channel.send(f"<@&{new_mute}> has been set as the mute role")
