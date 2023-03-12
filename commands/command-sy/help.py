# type: ignore
import config
import discord
from discord import Colour
import os

async def run(client, message, user_ping, args):

    if message.author.bot:
        return

    if not message.author.guild_permissions.administrator:

        command_files_usr = os.listdir('commands/command-usr')
        commands_usr = [f[:-3] for f in command_files_usr if f.endswith('.py')]

        embed = discord.Embed(title="Here's what i can do")
        embed.add_field(name='My Prefix:', value='\n' + config.PREFIX)
        embed.add_field(name='Useful Commands:', value='\nhelp' + '\nrank' + '\ntiemr' + '\nmembers')
        embed.add_field(name='\nGif/Action commands:', value='\n'.join(commands_usr))
        embed.color = Colour(int('FF69B4', 16))

        await message.author.send(embed=embed)

    else:

        command_files_usr = os.listdir('commands/command-usr')
        commands_usr = [f[:-3] for f in command_files_usr if f.endswith('.py')]

        command_files_sy = os.listdir('commands/command-sy')
        commands_sy = [f[:-3] for f in command_files_sy if f.endswith('.py') and f != 'rank.py' and f != 'help.py' and f != 'members.py' and f != 'kick.py' and f != 'ban.py' and f != 'mute.py']

        embed = discord.Embed(title="Here's what i can do")
        embed.add_field(name='My Prefix:', value='\n' + config.PREFIX + '\n', inline=True)
        embed.add_field(name='Useful Commands:', value='\nhelp' + '\nrank' + '\ntimer' + '\nmembers')
        embed.add_field(name='\nGif/Action Commands:', value='\n'.join(commands_usr), inline=True)
        embed.add_field(name='\nModeration Commands:', value='\n' + 'mute' + '\nkick' + '\nban', inline=True)
        embed.add_field(name='\nAdmin Commands:', value='\n'.join(commands_sy))
        embed.color = Colour(int('FF69B4', 16))

        await message.author.send(embed=embed)