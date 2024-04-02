from pyrogram import Client

from bot import config
from bot.client.ClientManager import ClientManager
from bot.scheduler.scheduler import AsyncScheduler
from db.connection import session, DefaultSpamValue, RentChannelSource, SellChannelSource, Admin

clientManager = ClientManager()

for i in range(len(config.api_ids)):
    app = Client(f"my_account{i+1}", api_id=config.api_ids[i], api_hash=config.api_hashes[i], workdir='bot/client/sessions')
    clientManager.add_client(app)

bot = Client("bot", api_id=config.api_ids[0], bot_token=config.BOT_TOKEN, workdir='bot/client/sessions')


scheduler = AsyncScheduler()

# Добавление начальных данных
try:
    if not session.query(DefaultSpamValue).first(): session.add(DefaultSpamValue())
    if not session.query(RentChannelSource).first(): session.add(RentChannelSource(id=-1))
    if not session.query(SellChannelSource).first(): session.add(SellChannelSource(id=-1))
    for admin in config.admins:
        if not session.query(Admin).filter_by(id=str(admin)).first():
            session.add(Admin(id=str(admin)))
    session.commit()
except:
    ...