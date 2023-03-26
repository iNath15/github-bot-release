import config

async def run(bot, message, args, user_ping):
    await message.channel.send(f'{config.MUTE_ROLE}')