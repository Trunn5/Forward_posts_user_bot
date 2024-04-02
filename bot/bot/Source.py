from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.bot.fsm import fsm, fsm_filter
from bot.utils.loader import bot, clientManager
from db.connection import session, RentChannelSource, SellChannelSource


@bot.on_message(filters.regex("🔗Источник"))
async def source(client: Client, message: Message):
    """Обработчик кнопки источник"""
    k = ReplyKeyboardMarkup(keyboard =
                            [[KeyboardButton("✏️Изменить ПРОДАЖА"),
                              KeyboardButton("✏️Изменить АРЕНДА")]])
    fsm[message.from_user.id] = "source"

    text = "Канал продажи: "
    try:
       text += (await clientManager.clients[0].get_chat(int(session.query(SellChannelSource).first().id))).title + '\n'
    except Exception as e:
        text += "Не удалось найти канал\n"
    text += "Канал аренды: "
    try:
        text += (await clientManager.clients[0].get_chat(int(session.query(RentChannelSource).first().id))).title
    except:
        text += "Не удалось найти канал\n"
    await message.reply(text, reply_markup=k)


@bot.on_message(filters.regex("✏️Изменить ПРОДАЖА") & fsm_filter("source"))
async def source_change_sell(client: Client, message: Message):
    """Обработчик кнопки изменить канал продажи"""
    fsm[message.from_user.id] += "_change_sell"
    await message.reply("Отправьте id канала для источника продаж.")


@bot.on_message(filters.text & fsm_filter("source_change_sell"))
async def source_changing_sell(client: Client, message: Message):
    """Измененние канала продажи"""
    try:
        ch_id = message.text
        ch = session.query(SellChannelSource).first()
        ch.id = ch_id
        session.commit()
        info = await clientManager.clients[0].get_chat(int(ch_id))
        fsm[message.from_user.id] = ''
        await message.reply(f"Канал для продаж: {info.title}  - успешно обновлен")
    except Exception as e:
        await message.reply(f"Ошибка! {e}")


@bot.on_message(filters.regex("✏️Изменить АРЕНДА") & fsm_filter("source"))
async def source_change_rent(client: Client, message: Message):
    """Обработчик кнопки изменения канала аренды"""
    fsm[message.from_user.id] += "_change_rent"
    await message.reply("Отправьте id канала для источника аренды.")


@bot.on_message(filters.text & fsm_filter("source_change_rent"))
async def source_changing_rent(client: Client, message: Message):
    """Изменение канала аренды"""
    try:
        ch_id = message.text
        ch = session.query(RentChannelSource).first()
        ch.id = ch_id
        session.commit()
        info = await clientManager.clients[0].get_chat(int(ch_id))
        fsm[message.from_user.id] = ''
        await message.reply(f"Канал для аренды: {info.title}  - успешно обновлен")
    except Exception as e:
        await message.reply(f"Ошибка! {e}")
