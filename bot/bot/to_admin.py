import asyncio

from pyrogram.errors import FloodWait

from bot import config
from bot.utils.loader import bot


async def to_admin(text: str):
    """Разослать в боте сообщение админам"""
    for admin in config.admins:
        try:
            await bot.send_message(int(admin), text, parse_mode="html")
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await bot.send_message(admin, text)
        except:
            print(f"не удалось отправить сообщение админу {admin}")
