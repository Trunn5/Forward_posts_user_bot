from pyrogram import Client, filters

from bot import config
from bot.ClientManager import ClientManager
from bot.scheduler import AsyncScheduler


clientManager = ClientManager()

for i in range(len(config.api_ids)):
    app = Client(f"my_account{i+1}", api_id=config.api_ids[i], api_hash=config.api_hashes[i], workdir='bot/sessions')
    clientManager.add_client(app)

bot = Client("bot", api_id=config.api_ids[0], bot_token=config.BOT_TOKEN, workdir='bot/sessions')


scheduler = AsyncScheduler()
