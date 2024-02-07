import asyncio

from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message

from bot import config
from bot.loader import app1, app2, scheduler
from pyrogram import filters

from bot.sending import is_valid_time_format, sending


@app1.on_message(filters.chat([config.rent_channel_id, config.sell_channel_id]))
@app2.on_message(filters.chat([config.rent_channel_id, config.sell_channel_id]))
async def new_posts(client, message: Message):
    """
    Обрабатывает новые посты в каналах, моментально пересылает в группы
    """
    for spam_group in config.groups_to_spam:
        try:
            await app1.copy_message(chat_id=spam_group, from_chat_id=message.chat.id, message_id=message.id)
        except PeerIdInvalid as e:
            for admin in config.admins:
                await app1.send_message(admin, parse_mode=ParseMode.HTML,
                                       text=f"<a href=https://docs.pyrogram.org/api/errors/bad-request#:~:text=is%20currently%20limited-,PEER_ID_INVALID,-The%20peer%20id>ОШИБКА.</a>\n"
                                            f"Познакомьтесь с чатом id: {spam_group}")


@app1.on_message(filters.chat(config.admins) & filters.command('current'))
@app2.on_message(filters.chat(config.admins) & filters.command('current'))
async def current_tasks(client, message: Message):
    """Присылает текущие таймслоты на пересылку"""
    text = "Текущие расписание постов:\n" + '\n'.join([time for _, time, _ in scheduler.tasks])
    if len(scheduler.tasks) == 0: text += "Пусто"
    await message.reply(text)


@app1.on_message(filters.chat(config.admins) & filters.command('add'))
@app2.on_message(filters.chat(config.admins) & filters.command('add'))
async def add(client, message: Message):
    """Добавление нового времени"""
    if len(message.command) < 2 or not is_valid_time_format(message.command[1]):
        await message.reply("Введите /add HH:MM")
        return
    time = message.command[1]

    await scheduler.add_task(task=sending, run_time=time)
    await current_tasks(app1, message)


@app1.on_message(filters.chat(config.admins) & filters.command('delete'))
@app2.on_message(filters.chat(config.admins) & filters.command('delete'))
async def delete(client, message: Message):
    """Удаление нового времени"""
    if len(message.command) < 2 or not is_valid_time_format(message.command[1]):
        await message.reply("Введите /add HH:MM")
        return
    time = message.command[1]
    if await scheduler.remove_task(sending, time):
        await message.reply(f"Успешно удалено время {time}")
    await current_tasks(client, message)

