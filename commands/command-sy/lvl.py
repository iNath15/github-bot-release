import csv
import asyncio

async def run(bot, message, args, user_ping):

    # Check if the user has administrator privileges
    if not message.author.guild_permissions.administrator:
        await message.channel.send('You need to be an admin to use this command.')
        return

    await message.channel.send("what would you like to make the base value for the XP?\n100 is reccomended for most")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await bot.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    xp_value = int(float(response.content))
    xp = xp_value

    await message.channel.send("by how much would you like each level to increase?\n3-5% is reccomended")

    # Wait for the user's response
    def check(m):
        return m.channel == message.channel and m.author == message.author
    try:
        response = await bot.wait_for('message', check=check, timeout=20.0)
    except asyncio.TimeoutError:
        await message.channel.send("You didn't respond in time.")
        return

    increase_value = int(float(response.content))
    lvl = ((increase_value / 100) + 1)


    table = [['level', 'xp']]
    for i in range(1,1001):
        if i == 1:
            table.append([i, xp])
        else:
            prev_xp = table[i-1][1]
            xp = int((prev_xp*lvl) + xp_value)
            table.append([i, xp])

    with open('rank-lvl.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table)

    await message.channel.send(f"You're values have been set, base xp = {xp_value}, level increase = {increase_value}")