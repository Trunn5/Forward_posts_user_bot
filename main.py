from pyrogram import compose

from bot.utils.loader import bot, clientManager
from bot import *

if __name__ == '__main__':
    print("Bot started.")
    compose(clientManager.clients+[bot])
