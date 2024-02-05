from pyrogram import Client

from bot import config
from bot.scheduler import AsyncScheduler

api_id = config.API_ID
api_hash = config.API_HASH

app = Client("my_account", api_id=api_id, api_hash=api_hash)

scheduler = AsyncScheduler()
