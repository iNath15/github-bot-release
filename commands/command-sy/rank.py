# type: ignore
import csv
import ranklist
import discord

def progress_bar(value, max_value, size):
    percentage = value / max_value
    progress = round(size * percentage)
    empty_progress = size - progress

    progress_text = '▇' * progress
    empty_progress_text = '—' * empty_progress
    percentage_text = str(round(percentage * 100)) + '%'

    bar = f'[{progress_text}{empty_progress_text}] {percentage_text}'

    return bar

async def run(bot, message, user_ping, args):
    if user_ping:
        user_id = str(user_ping.id)
    else:
        user_id = str(message.author.id)



    user_data = ranklist.RANK_DATA.get(user_id)
    if user_data:
        levels = []
        with open('rank-lvl.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                levels.append(row)
        levels = levels[1:]  # remove the header row
        current_xp = user_data
        for i in range(len(levels)):
            if int(levels[i][1]) > current_xp:
                level = i
                xp_needed = int(levels[i][1]) - current_xp
                break
            current_xp -= int(levels[i][1])
        else:
            level = len(levels)
            xp_needed = 0
        # calculate the percentage of XP earned
        percentage = current_xp / int(levels[level][1])
        # call the progress_bar function
        bar = progress_bar(percentage, 1, 15)

        user = message.author if not user_ping else user_ping
        embed = discord.Embed(title=f"{user.name}, you're level {level}", color=0x0096FFF)
        embed.add_field(name=f"You need {xp_needed}xp to reach level {level + 1}", value=f'```json\n"{bar}"\n```')
        await message.channel.send(embed=embed)
    else:
        user = message.author if not user_ping else user_ping
        embed2 = discord.Embed(title=f"{user.name}, you don't have any xp yet")
        await message.channel.send(embed=embed2)
