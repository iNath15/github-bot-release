# type: ignore
import discord
import os
import random
import pathlib

sent_files = []

async def run(bot, message, user_ping, args):
    file_name = pathlib.Path(__file__).name
    base_name = os.path.basename(file_name)
    file_path, extension = base_name.split('.')
    image_folder_path = 'commands/images/{}'.format(file_path)
    text_folder_path = 'commands/text/{}'.format(file_path)
    color_folder_path = 'commands/color/{}'.format(file_path)
    cwd = os.getcwd()
    image_full_path = os.path.join(cwd, image_folder_path)
    text_full_path = os.path.join(cwd, text_folder_path)
    color_full_path = os.path.join(cwd, color_folder_path)
    image_files = os.listdir(image_full_path)
    text_files = os.listdir(text_full_path)
    if not image_files and not text_files:
        await message.channel.send("This command does not contain any content.")
        return
    image_file = random.choice(image_files) if image_files else None
    text_file = random.choice(text_files) if text_files else None
    
    while image_file in sent_files and image_files:
        image_file = random.choice(image_files)
    file_extension = pathlib.Path(image_file).suffix if image_file else ""
    text = ""
    if text_file:
        with open(os.path.join(text_full_path, text_file), 'r') as f:
            text = f.read()
    
    color_value = ""
    color_files = os.listdir(color_full_path)
    if color_files:
        with open(os.path.join(color_full_path, color_files[0]), 'r') as f:
            color_value = f.read()

    if text and image_file:
        embed = discord.Embed(title=text)
        if color_value:
            embed.color = int(color_value.replace("#", "0x"), 16)
        embed.set_image(url='attachment://image' + file_extension)
        await message.channel.send(file=discord.File(os.path.join(image_full_path, image_file), filename='image' + file_extension), embed=embed)
    elif text:
        embed = discord.Embed(title=text)
        if color_value:
            embed.color = int(color_value.replace("#", "0x"), 16)
        await message.channel.send(embed=embed)
    elif image_file:
        embed = discord.Embed()
        if color_value:
            embed.color = int(color_value.replace("#", "0x"), 16)
        embed.set_image(url='attachment://image' + file_extension)
        await message.channel.send(file=discord.File(os.path.join(image_full_path, image_file), filename='image' + file_extension), embed=embed)
    sent_files.append(image_file)
    if len(sent_files) == len(image_files):
        sent_files.clear()