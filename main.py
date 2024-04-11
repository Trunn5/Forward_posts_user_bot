from pyrogram import compose

from bot.utils.loader import bot_client, clientManager
from bot import *

if __name__ == '__main__':
    print("Bot started.")
    compose([x.client for x in clientManager.clients]+[bot_client])
