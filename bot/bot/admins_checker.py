from pyrogram import Client
from pyrogram.types import Message

from bot.utils.loader import bot
from db.connection import session, Admin


@bot.on_message()
async def admin_checker(client: Client, message: Message):
    if str(message.from_user.id) in [x.id for x in session.query(Admin).all()]:
        await message.continue_propagation()
