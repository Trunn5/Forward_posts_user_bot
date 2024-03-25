import asyncio

from pyrogram import filters
from pyrogram.types import Message

from bot import config
from bot.loader import clientManager


@(clientManager.clients[0]).on_message(filters.user(config.admins), filters.command('sbor'))
async def message(message: Message):
    await message.delete()
    with open(f"{message.chat.title}.txt", 'w') as f:
        print("Sbor userov s grupi: ", message.chat.title)
        async for member in message.chat.get_members():
            try:
                f.write(f"{member.user.username}\n")
                await asyncio.sleep(0.02)
            except:
                await asyncio.sleep(25)
