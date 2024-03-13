import asyncio

from pyrogram import compose

from bot import config
from bot.loader import app1, app2

from bot import handlers
from bot import album_handler

def main():
    print("Bot started.")
    compose([app1, app2])


if __name__ == '__main__':
    main()
