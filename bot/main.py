import asyncio

from pyrogram import compose
from bot.loader import app1, app2

import handlers


async def main():
    print("Bot started.")
    await compose([app1, app2])


if __name__ == '__main__':
    asyncio.run(main())
