# type: ignore
import config
import asyncio


async def run(bot, message, user_ping, args):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send("Would you like to display the unknown command message. \n**yes**, **no**?")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await bot.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    # Set the prefix to the user's response
    answer = response.content.lower()

    # Read the contents of the config.py file
    with open('config.py', 'r') as f:
        config_contents = f.read()

    # Replace the value of the PREFIX variable with the new prefix
    config_contents = config_contents.replace(f'UNKNOWN = "{config.UNKNOWN}"', f'UNKNOWN = "{answer}"')

    # Write the modified contents back to the config.py file
    with open('config.py', 'w') as f:
        f.write(config_contents)

    # Update the PREFIX variable in the config module
    config.UNKNOWN = answer

    # Send a message confirming the change
    if config.UNKNOWN == "yes":
        await message.channel.send("The Unknown command message has been enabled")
    else:
        await message.channel.send("The Unknown command message has been disabled")
