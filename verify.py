#type: ignore
import discord
import config
import discord.ui
from discord.ext import commands

intents = discord.Intents.all()
# bot = discord.bot(intents=intents)

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

class VerifyButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.green, custom_id='verify_button')
    async def click(self, interaction: discord.Interaction, Button: discord.ui.Button):

        role = config.ROLE

        if config.ROLE in [y.id for y in interaction.user.roles]:
            await interaction.user.remove_roles(interaction.user.guild.get_role(role))
            await interaction.response.send_message("You've unverified yourself", ephemeral = True)

        else:
            await interaction.user.add_roles(interaction.user.guild.get_role(role))
            await interaction.response.send_message("You've been verified", ephemeral = True)

class VerifyViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=config.PREFIX, intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(VerifyButton())

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

    bot.add_view(VerifyButton())

@bot.event
async def on_message(message):
    if message.content.lower().startswith(f'{config.PREFIX}verify'):
        embed = discord.Embed(title="Verify!", description="Read the rule, and press the button to Verify!")
        await message.channel.send(embed=embed, view=VerifyButton())


bot.run(config.TOKEN)
