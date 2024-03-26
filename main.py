from pyrogram import compose, filters

from bot import config
from bot.album_handler import on_media_group
from bot.loader import bot, clientManager

from bot import album_handler
from bot.bot import handlers



if __name__ == '__main__':
    print("Bot started.")
    compose(clientManager.clients+[bot])
