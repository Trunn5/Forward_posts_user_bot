from pyrogram import Client

from bot import config
from bot.client.ClientManager import ClientManager, MyClient
from bot.scheduler.scheduler import AsyncScheduler

clientManager = ClientManager()

for i in range(len(config.api_ids)):
    app = Client(f"my_account{i+1}", api_id=config.api_ids[i], api_hash=config.api_hashes[i], workdir='sessions')
    clientManager.add_client(app)

bot_client = Client("bot", api_id=config.api_ids[0], bot_token=config.BOT_TOKEN, api_hash=config.api_hashes[0], workdir='sessions')
bot = MyClient(bot_client)
scheduler = AsyncScheduler()
