import asyncio

from pyrogram import filters, Client
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.bot.Start import start
from bot.bot.fsm import fsm, fsm_filter
from bot.bot.to_admin import to_admin
from bot.utils.loader import bot_client, clientManager
from db.connection import session, SellChannelForward


@bot_client.on_message(filters.regex("💰Продажа"))
async def sell(client: Client, message: Message):
    """Обработчик кнопки продажа"""
    k = ReplyKeyboardMarkup(keyboard =
                            [[KeyboardButton("➕Добавить")],
                              [KeyboardButton("➖Удалить")],
                              [KeyboardButton("✏️Изменить")],
                              [KeyboardButton("🔙Назад")]],
                            resize_keyboard=True)
    fsm[message.from_user.id] = "sell"
    text = "Каналы продажи:\n"

    for chn in session.query(SellChannelForward).all():
        text += f"{chn.id}: {chn.title} - {chn.get_interval} с." + '\n'

    await message.reply(text, reply_markup=k)


@bot_client.on_message(filters.regex("➕Добавить") & fsm_filter("sell"))
async def sell_add(client: Client, message: Message):
    """Обработчик кнопки добавить канал продаж."""
    fsm[message.from_user.id] += "_add"
    await message.reply("Отправьте id канала для перессылки продаж.")


@bot_client.on_message(filters.text & fsm_filter("sell_add"))
async def sell_adding(client: Client, message: Message):
    """Добавление канада продаж."""
    try:
        ch_id = message.text

        if session.query(SellChannelForward).filter_by(id=ch_id).first() != None:
            raise "Такой чат уже добавлен."

        while True:
            user_bot = clientManager.get_worker()
            try:
                info = await user_bot.get_chat(int(ch_id.split('_')[0]))
                break
            except ChannelInvalid as e:
                await to_admin(f"<b>Ошибка:</b> Юзер-бот {(await user_bot.get_me()).id} не может получить данные о чате"
                               f" {ch_id}: {ch_id}")

        session.add(SellChannelForward(id=ch_id, title=info.title))
        session.commit()
        fsm[message.from_user.id] = ''
        await message.reply(f"✅Канал {info.title} успешно добавлен")
        await start(client, message)
    except PeerIdInvalid as e:
        await message.reply(f"⛔️<b>Ошибка:</b> Неверный айди чата.\n⚙️ Тип:\n{e}")
    except Exception as e:
        await message.reply(f"⛔️Ошибка!\n{e}")


@bot_client.on_message(filters.regex("➖Удалить") & fsm_filter("sell"))
async def sell_rm(client: Client, message: Message):
    """Обработчик кнопки удаления канада продаж."""
    fsm[message.from_user.id] += "_rm"
    await message.reply("Отправьте id канала для перессылки продаж.")


@bot_client.on_message(filters.text & fsm_filter("sell_rm"))
async def sell_rming(client: Client, message: Message):
    """Удаление канала для продаж из списка."""
    try:
        ch_id = message.text
        ch = session.query(SellChannelForward).filter_by(id=ch_id).first()
        if ch is None:
            raise Exception(f"Нет канала {ch_id} для удаления")
        session.delete(ch)
        session.commit()
        info = await clientManager.clients[0].get_chat(int(ch_id.split('_')[0]))
        fsm[message.from_user.id] = ''
        await message.reply(f"Канал {info.title} успешно УДАЛЕН.")
        await start(client, message)
    except Exception as e:
        await message.reply(f"⛔️Ошибка:\n{e.__cause__}\n"
                            f"⚙️Тип:\n{e}")


@bot_client.on_message(filters.regex("✏️Изменить") & fsm_filter("sell"))
async def sell_change(client: Client, message: Message):
    """Обработчик кнопки изменить"""
    fsm[message.from_user.id] += '_change'
    await message.reply("Отправьте айди чата и новый интервал (в секундах), например:\n"
                        "-100123123 60")


@bot_client.on_message(filters.text & fsm_filter("sell_change"))
async def sell_changing(client: Client, message: Message):
    """Изменение интервала пересылки у чата"""
    try:
        chat_id, interval = message.text.split()
        ch = session.query(SellChannelForward).filter_by(id=chat_id).first()
        ch.interval = int(interval)
        session.commit()
        fsm[message.from_user.id] = ''
        await message.reply(f"успешно изменено на {interval}!")
        await sell(client, message)
    except Exception as e:
        await message.reply(f"⛔️Ошибка:\n{e.__cause__}\n"
                            f"⚙️Тип:\n{e}")
