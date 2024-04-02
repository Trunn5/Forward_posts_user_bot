import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.bot.Start import start
from bot.bot.fsm import fsm, fsm_filter
from bot.bot.to_admin import to_admin
from bot.utils.loader import bot, clientManager
from db.connection import session, RentChannelForward, DefaultSpamValue


@bot.on_message(filters.regex("⏱Глобальный интервал"))
async def globalinterval(client: Client, message: Message):
    """Обработчик кнопки глобальный интервал"""
    k = ReplyKeyboardRemove()
    fsm[message.from_user.id] = "globalinterval"
    text = (f"Текущий интервал: {session.query(DefaultSpamValue).first().value}\n"
            f"Чтобы изменить напишите новое число, для выхода /start")
    await message.reply(text, reply_markup=k)


@bot.on_message(filters.text & fsm_filter("globalinterval"))
async def globalinterval_changing(client: Client, message: Message):
    """Изменение глобального интервала"""
    try:
        session.query(DefaultSpamValue).first().value = int(message.text)
        session.commit()
    except Exception as e:
        await message.reply(f"Ошибка! {e}")
        return

    fsm[message.from_user.id] = ""
    await globalinterval(client, message)
