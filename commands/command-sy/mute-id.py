import config

async def run(client, message, args, user_ping):
    await message.channel.send(f'{config.MUTE_ROLE}')