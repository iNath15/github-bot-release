# type: ignore
from PIL import Image, ImageDraw, ImageFont
import requests
import discord
import config
from io import BytesIO
import os


def generate_leave_image(member):
    # Download the member's profile picture
    response = requests.get(member.avatar.url)
    profile_picture = Image.open(BytesIO(response.content))

    # Resize the profile picture to a square
    profile_picture = profile_picture.resize((300, 300)).convert('RGBA')
    mask = Image.new('L', profile_picture.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 300, 300), fill=255)
    profile_picture.putalpha(mask)

    # Load the background image
    background = Image.open('goodbye.jpg')
    background = background.convert('RGBA')
    max_height = 600
    if background.height > max_height:
        scale_factor = max_height / background.height
        new_width = int(background.width * scale_factor)
        background = background.resize((new_width, max_height), resample=Image.LANCZOS)

    # Add the semi-transparent black square
    overlay = Image.new('RGBA', (background.size), (0, 0, 0, 153))
    draw = ImageDraw.Draw(overlay)
    margin = 30
    draw.rectangle((margin, margin, new_width / 2, max_height / 2), fill=(0, 0, 0, 153))

    # Add the semi-transparent black square overlay to the image
    background.alpha_composite(overlay)

    # Add the profile picture to the center of the background image
    x = int((background.width - profile_picture.width) / 2)
    y = int((background.height - profile_picture.height) / 2)
    background.alpha_composite(profile_picture, (x, y))

    # Add the leave text to the image
    draw = ImageDraw.Draw(background)
    font_path = "font/" + config.FONT
    font = ImageFont.truetype(font_path, size=46)
    leave_text = 'Goodbye!'
    leave_text_width, leave_text_height = draw.textsize(leave_text, font)
    leave_x = int((background.width - leave_text_width) / 2)
    leave_y = y + profile_picture.height + 50
    draw.text((leave_x, leave_y), leave_text, font=font, fill=(255, 255, 255))

    name_text = member.name
    name_text_width, name_text_height = draw.textsize(name_text, font)
    name_x = int((background.width - name_text_width) / 2)
    name_y = y - 80
    draw.text((name_x, name_y), name_text, font=font, fill=(255, 255, 255))

    # Save the image
    filename = f'leave-{member.id}.png'
    background.save(filename)

    return filename


async def on_member_remove(bot, member):
    channel = member.guild.get_channel(config.GOODBYE_CHL)
    filename = generate_leave_image(member)
    with open(filename, 'rb') as f:
        file = discord.File(filename)
        message = f"> Goodbye {member.mention}, we're sad to see you go."
        await channel.send(message, file=file)
    os.remove(filename)
