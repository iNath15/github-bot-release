# type: ignore
import discord
import importlib
import asyncio
import config
import re
from datetime import timedelta
import random
import ranklist
import discord.ui
from discord.ext import commands




# Enable all intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)
#client.debug = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

# Keep track of which users are AFK
afk_users = {}




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

#confirm the bot is online in the terminal and set the status of the bot
@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')
    bot.add_view(VerifyButton())

    # # Set the status
    # if config.STATUS_TYPE == 1:
    #     game = discord.Game(f'{config.STATUS}')
    #     await client.change_presence(activity=game)
    # elif config.STATUS_TYPE == 2:
    #     stream = discord.Streaming(name=config.STATUS, url=config.STATUS_URL)
    #     await client.change_presence(activity=stream)
    # elif config.STATUS_TYPE == 3:
    #     listen = discord.Activity(type=discord.ActivityType.listening, name=config.STATUS)
    #     await client.change_presence(activity=listen)
    # elif config.STATUS_TYPE == 4:
    #     watch = discord.Activity(type=discord.ActivityType.watching, name=config.STATUS)
    #     await client.change_presence(activity=watch)
    # else:
    #     listen = discord.Activity(type=discord.ActivityType.listening, name="Kessoku band")
    #     await client.change_presence(activity=listen)

    game = discord.Game(f'{config.STATUS}')
    await client.change_presence(activity=game)

@client.event
async def verify(message):
    if message.content.lower().startswith(f'{config.PREFIX}verify'):
        print("ping command executed")
        embed = discord.Embed(title="Verify!", description="Read the rule, and press the button to Verify!")
        try:
            await message.channel.send(embed=embed, view=VerifyButton())
        except Exception as e:
            print(f"Error sending message: {e}")




async def user_ping(message):
    for mention in message.mentions:
        if mention.id in afk_users:
            await message.channel.send(f"**{mention}** is AFK.")



# @client.event
# async def on_member_join(member):
#     if config.WELCOME == "on":
#         await welcome.on_member_join(client, member)







#bot timer, command handler, and help
@client.event
async def on_message(message):

    # cooldown for rank
    cooldown = {}

    import time


    if message.author.bot:
        return
        

    elif message.content.lower().startswith(f'{config.PREFIX}'):

        if message.author.bot:
            return

        # Strip the message content of the ping
        stripped_content = message.content
        for mention in message.mentions:
            stripped_content = stripped_content.replace(mention.mention, '')

        # Get the command name, additional arguments and user ping
        command = stripped_content[len(f'{config.PREFIX}'):].strip().lower().split()[0]
        user_ping = message.author.mention
        args = stripped_content[len(f'{config.PREFIX} {command}'):].strip()


        if command == "timer":
            # Extract the time string from the message
            time_string = message.content[6:].strip()
            
            # Define regex patterns for hours, minutes, and seconds
            hours_pattern = re.compile(r"(\d+)h")
            minutes_pattern = re.compile(r"(\d+)m")
            seconds_pattern = re.compile(r"(\d+)s")

            # Extract the hours, minutes, and seconds from the time string
            hours = int(hours_pattern.search(time_string).group(1)) if hours_pattern.search(time_string) else 0
            minutes = int(minutes_pattern.search(time_string).group(1)) if minutes_pattern.search(time_string) else 0
            seconds = int(seconds_pattern.search(time_string).group(1)) if seconds_pattern.search(time_string) else 0
            
            if hours>24 or minutes>60 or seconds>60:
                await message.channel.send("Invalid time. use the time format: ``0h 0m 0s``")
                return

            if hours == 0 and minutes == 0 and seconds == 0:
                await message.channel.send("Please specify a valid time. ")
                return
                
            # Create a timedelta object from the hours, minutes, and seconds
            time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            await message.channel.send(f"Timer set for {time}")
            await asyncio.sleep(time.total_seconds())

            # Send a message to the user when the timer is done
            await message.channel.send(f"{message.author.mention} Your timer has finished!")
            return

        # elif command == "verify":
        #     button_view = VerifyButton()
        #     await message.channel.send("Click the button:", view=button_view)

        elif message.content.lower().startswith(f'{config.PREFIX}afk'):
            if message.author.id in afk_users:
                del afk_users[message.author.id]
                await message.channel.send(f"**{message.author}** is no longer AFK.")
            else:
                afk_users[message.author.id] = message.author
                await message.channel.send(f"**{message.author}** is now AFK.")


            
        else:
            module_name = f'{command}'
            try:
                module = importlib.import_module(f'commands.command-usr.{module_name}')
            except ModuleNotFoundError:
                try:
                    module = importlib.import_module(f'commands.command-sy.{module_name}')
                except ModuleNotFoundError:
                    if config.UNKNOWN == "yes":
                        await message.channel.send(f'Invalid command: {command}')
                        return
                    else:
                        return

            await module.run(client, message, args, user_ping)






    user_id = str(message.author.id)
    if user_id in cooldown:
        if time.time() - cooldown[user_id] < 60:
            # User is still on cooldown
            return
    else:
        cooldown[user_id] = time.time()

    if user_id in ranklist.RANK_DATA:
        ranklist.RANK_DATA[user_id] += random.randint(10, 20)
    else:
        ranklist.RANK_DATA[user_id] = 5

    # Write the RANK_DATA dictionary to the ranklist.py file
    with open("ranklist.py", "w") as f:
        f.write("RANK_DATA = " + str(ranklist.RANK_DATA))

    async def user_ping(message):
        for mention in message.mentions:
            if mention.id in afk_users:
                await message.channel.send(f"**{mention}** is AFK.")


    if message.mentions:
        await user_ping(message)

    if message.author.bot:
        return

    # only respond to messages that mention the bot
    elif client.user in message.mentions and not message.mention_everyone:

        # Only process commands from members (not bots)
        if message.author.bot:
            return

        await message.channel.send(f"try using `{config.PREFIX} help` if there's something you're unsure of")


# Token used to sign into the bot   
client.run(config.TOKEN)