# type: ignore
import discord
import discord.ui
from discord.ext import commands
import config
import bot.py
from bot.py import VerifyButton
# class VerifyButton(discord.ui.View):

#     def __init__(self):
#         super().__init__(timeout=None)

#     @discord.ui.button(label="Click me!", style=discord.ButtonStyle.green)
#     async def click(self, interaction: discord.Interaction, Button: discord.ui.Button):

#         role = config.ROLE

#         if config.ROLE in [y.id for y in interaction.user.roles]:
#             await interaction.user.remove_roles(interaction.user.guild.get_role(role))
#             await interaction.response.send_message("You've unverified yourself", ephemeral = True)
            
#         else:
#             await interaction.user.add_roles(interaction.user.guild.get_role(role))
#             await interaction.response.send_message("You've been verified", ephemeral = True)

async def run(client, message, user_ping, args):

    button_view = VerifyButton()
    await message.channel.send("Click the button:", view=button_view)

