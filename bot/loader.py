from pyrogram import Client

from bot import config
from bot.scheduler import AsyncScheduler

api_id_1 = config.API_ID_1
api_hash_1 = config.API_HASH_1
api_id_2 = config.API_ID_2
api_hash_2 = config.API_HASH_2

app1 = Client("my_account", api_id=api_id_1, api_hash=api_hash_1, workdir='bot')
app2 = Client("my_account2", api_id=api_id_2, api_hash=api_hash_2, workdir='bot')

scheduler = AsyncScheduler()
