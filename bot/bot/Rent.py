import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.bot.Start import start
from bot.bot.fsm import fsm, fsm_filter
from bot.bot.to_admin import to_admin
from bot.utils.loader import bot, clientManager
from db.connection import session, RentChannelForward


@bot.on_message(filters.regex("🏠Аренда"))
async def rent(client: Client, message: Message):
    """Обработчик кнопки Аренда"""
    k = ReplyKeyboardMarkup(keyboard =
                            [[KeyboardButton("➕Добавить"),
                              KeyboardButton("➖Удалить"),
                              KeyboardButton("✏️Изменить")]])
    fsm[message.from_user.id] = "rent"
    text = "Каналы Аренды:\n"
    for chn in session.query(RentChannelForward).all():
        try:
            ch_id = int(chn.id.split('_')[0])
            text += f"{chn.id}: " + (await clientManager.clients[0].get_chat(ch_id)).title + \
                    f" - {chn.get_interval} с." + '\n'
            await asyncio.sleep(0.11)
        except Exception as e:
            await to_admin(f"ОШИБКА: Не могу получить данные о чате {chn}: {e}")
    await message.reply(text, reply_markup=k)


@bot.on_message(filters.regex("➕Добавить") & fsm_filter("rent"))
async def rent_add(client: Client, message: Message):
    """Обработчик кнопки добавить канал аренды."""
    fsm[message.from_user.id] += "_add"
    await message.reply("Отправьте id канала для перессылки аренды.")


@bot.on_message(filters.text & fsm_filter("rent_add"))
async def rent_adding(client: Client, message: Message):
    """Добавление канала аренды."""
    try:
        ch_id = message.text
        info = await clientManager.clients[0].get_chat(int(ch_id.split('_')[0]))
        session.add(RentChannelForward(id=ch_id))
        session.commit()
        fsm[message.from_user.id] = ''
        await message.reply(f"Канал {info.title} успешно добавлен")
        await start(client, message)
    except Exception as e:
        await message.reply(f"Ошибка! {e}")


@bot.on_message(filters.regex("➖Удалить") & fsm_filter("rent"))
async def rent_rm(client: Client, message: Message):
    """Обработчик кнопки удаления канада Аренд."""
    fsm[message.from_user.id] += "_rm"
    await message.reply("Отправьте id канала для перессылки аренды.")


@bot.on_message(filters.text & fsm_filter("rent_rm"))
async def rent_rming(client: Client, message: Message):
    """Удаление канала для аренды из списка."""
    try:
        ch_id = message.text
        ch = session.query(RentChannelForward).filter_by(id=ch_id).first()
        if ch is None:
            raise Exception(f"Нет канала {ch_id} для удаления")
        session.delete(ch)
        session.commit()
        info = await clientManager.clients[0].get_chat(int(ch_id.split('_')[0]))
        fsm[message.from_user.id] = ''
        await message.reply(f"Канал {info.title} успешно УДАЛЕН.")
    except Exception as e:
        await message.reply(f"Ошибка!: {e}")


@bot.on_message(filters.regex("✏️Изменить") & fsm_filter("rent"))
async def rent_change(client: Client, message: Message):
    """Обработчик кнопки изменить"""
    fsm[message.from_user.id] += '_change'
    await message.reply("Отправьте айди чата и новый интервал (в секундах), например:\n"
                        "-100123123 60")


@bot.on_message(filters.text & fsm_filter("rent_change"))
async def rent_changing(client: Client, message: Message):
    """Изменение интервала пересылки у чата"""
    try:
        chat_id, interval = message.text.split()
        ch_id = session.query(RentChannelForward).filter_by(id=chat_id).first()
        ch_id.interval = int(interval)
        session.commit()
        fsm[message.from_user.id] = ''
        await message.reply(f"успешно изменено на {interval}!")
        await rent(client, message)
    except Exception as e:
        await message.reply("Ошибка!\ne")
