import config
import asyncio

async def run(client, message, user_ping, args):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send("What do you want to set the prefix to?")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await client.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    # Set the prefix to the user's response
    new_prefix = response.content

    # Check if the new prefix contains any symbols
    symbols = """$§!¡¯'"“”#§$€£¢%∞‰&™˜/¶\([{)}]=+?´`¨^~'*@º-_.:·÷,;„<>≤≥"""
    contains_symbols = False
    for symbol in symbols:
        if symbol in new_prefix:
            contains_symbols = True
            break

    # Add a space after the new prefix if it doesn't contain any symbols
    if not contains_symbols:
        new_prefix += " "

    # Read the contents of the config.py file
    with open('config.py', 'r') as f:
        config_contents = f.read()

    # Replace the value of the PREFIX variable with the new prefix
    config_contents = config_contents.replace(f'PREFIX = "{config.PREFIX}"', f'PREFIX = "{new_prefix}"')

    # Write the modified contents back to the config.py file
    with open('config.py', 'w') as f:
        f.write(config_contents)

    # Update the PREFIX variable in the config module
    config.PREFIX = new_prefix

    # Send a message confirming the change
    await message.channel.send(f"Prefix successfully changed to {new_prefix}")
