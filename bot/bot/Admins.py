from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.bot.fsm import fsm, fsm_filter
from bot.utils.loader import bot
from db.connection import session, Admin


@bot.on_message(filters.regex("👥Админы"))
async def admins(client: Client, message: Message):
    """Обработчик кнопки админы"""
    k = ReplyKeyboardMarkup(keyboard =
                            [[KeyboardButton("➕Добавить"),
                              KeyboardButton("➖Удалить")]])
    fsm[message.from_user.id] = "admins"
    text = "Текущие админы:\n"
    for admin in session.query(Admin).all():
        text += f"{admin.id}\n"
    await message.reply(text, reply_markup=k)


@bot.on_message(filters.regex("➕Добавить") & fsm_filter("admins"))
async def admins_add(client: Client, message: Message):
    """Обработчик кнопки добавить """
    fsm[message.from_user.id] += '_add'
    await message.reply("Отрпавьте id нового админа.")


@bot.on_message(filters.text & fsm_filter("admins_add"))
async def admins_adding(client: Client, message: Message):
    """Добавление нового админа"""
    try:
        session.add(Admin(id=message.text))
        session.commit()
        fsm[message.from_user.id] += ''
        await message.reply(f"Админ {message.text} добавлен.")
        await admins(client, message)
    except Exception as e:
        await message.reply(f"Ошибка! {e}")


@bot.on_message(filters.regex("➖Удалить") & fsm_filter("admins"))
async def admins_rm(client: Client, message: Message):
    """Обработчик кнопки добавить """
    fsm[message.from_user.id] += '_rm'
    await message.reply("Отрпавьте id нового админа.")


@bot.on_message(filters.text & fsm_filter("admins_rm"))
async def admins_rming(client: Client, message: Message):
    """Добавление нового админа"""
    try:
        obj = session.query(Admin).filter_by(id=message.text).first()
        session.delete(obj)
        session.commit()
        fsm[message.from_user.id] += ''
        await message.reply(f"Админ {message.text} удален.")
        await admins(client, message)
    except Exception as e:
        await message.reply(f"Ошибка! {e}")
