import discord
from discord import Colour
import os

async def run(bot, message, user_ping, args):
    if message.author.bot:
            return

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    # Get a list of all the files in the "commands/command-usr" and "commands/command-usr2" directories
    command_files = os.listdir('commands/command-usr')
    # Extract the command names from the file names
    commands = [f[:-3] for f in command_files if f.endswith('.py')]

    # Create an embed message to display the list of commands
    embed = discord.Embed(title='user created commands')
    embed.add_field(name='Commands:', value='\n'.join(commands))
    embed.color = Colour(int('FF69B4', 16))  # Pink

    

    # Send the embed message
    await message.channel.send(embed=embed)