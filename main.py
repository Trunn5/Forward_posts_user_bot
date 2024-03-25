import asyncio
import multiprocessing

from pyrogram import compose, filters

from bot import config
from bot.album_handler import on_media_group
from bot.loader import bot, clientManager

from bot import album_handler
from bot.bot import handlers

from pyrogram.handlers import MessageHandler




async def run_bot():
    print('bot is started')
    await dp.start_polling(bot)
    print('bot is stopped')
class AsyncBotProcess(multiprocessing.Process):
    def run(self):
        asyncio.run(run_bot())

async def run_clients():
    print("clients are started")
    await compose([app1, app2])
    print('clients are stopped')

async def main():
    print('main')
    await asyncio.gather(run_bot(), run_clients())



if __name__ == '__main__':
    # AsyncBotProcess().start()
    # asyncio.run(main())
    # multiprocessing.Process(target=asyncio.run, args=(run_bot(),)).start()
    print("Bot started.")
    compose(clientManager.clients+[bot])
