import asyncio

from pyrogram.errors import Flood, FloodWait

from bot import config
from bot.loader import bot


async def to_admin(text: str):
    for admin in config.admins:
        try:
            await bot.send_message(admin, text)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await bot.send_message(admin, text)
        except:
            print(f"не удалось отправить сообщение админу {admin}")