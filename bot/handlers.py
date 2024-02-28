import asyncio
from pprint import pprint

from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message

from bot import config
from bot.loader import app1, app2, scheduler, clear_dailys
from pyrogram import filters

from bot.sending import is_valid_time_format, sending, check_stop_sign, forward_post, recently_media_groups, \
    clear_daily, get_number_posts, set_number_posts

SEND = True


@app1.on_message(filters.chat(config.rent_channel_id))
async def new_post_rent(client, message: Message):
    """
    Обрабатывает новые посты в канале для аренды, моментально пересылает в группы для аренды
    """
    if not SEND:
        return
    # проверяем что такую медиа группу мы уже отправили
    if message.media_group_id and message.media_group_id in recently_media_groups:
        return
    else: # добавляем новую media группу в множество недавних
        if len(recently_media_groups) > 10:
            recently_media_groups.clear()
        recently_media_groups.add(message.media_group_id)

    # ждём прогрузки данных в телеграмме
    await asyncio.sleep(5)

    await forward_post(client, message, config.groups_for_rent)


# @app1.on_message(filters.chat(config.sell_channel_id))
# async def new_post_sell(client, message: Message):
#     """
#     Обрабатывает новые посты в канале для продажи, моментально пересылает в группы для продажи
#     """
#     if not SEND:
#         return
# # проверяем что такую медиа группу мы уже отправили
#     if message.media_group_id and message.media_group_id in recently_media_groups:
#         return
#     else: # добавляем новую media группу в множество недавних
#         if len(recently_media_groups) > 10:
#             recently_media_groups.clear()
#         recently_media_groups.add(message.media_group_id)
#
#     # ждём прогрузки данных в телеграмме
#     await asyncio.sleep(5)
#     await forward_post(client, message, config.groups_for_sell)


@app1.on_message(filters.chat(config.admins) & filters.command('current'))
@app2.on_message(filters.chat(config.admins) & filters.command('current'))
async def current_tasks(client, message: Message):
    """Присылает текущие таймслоты на пересылку"""
    text = "Текущие расписание постов:\n" + '\n'.join([time for _, time, _ in scheduler.tasks])
    if len(scheduler.tasks) == 0: text += "Пусто"
    # print(message.text)
    await message.reply(text)


@app1.on_message(filters.chat(config.admins) & filters.command('add'))
@app2.on_message(filters.chat(config.admins) & filters.command('add'))
async def add(client, message: Message):
    """Добавление нового времени"""
    if len(message.command) < 2 or not is_valid_time_format(message.command[1]):
        await message.reply("Введите /add HH:MM")
        return
    time = message.command[1]
    if len(clear_dailys.tasks) == 0:
        await clear_dailys.add_task(task=clear_daily, run_time="00:00")
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


@app1.on_message(filters.chat(config.admins) & filters.command('switch'))
@app2.on_message(filters.chat(config.admins) & filters.command('switch'))
async def switch(client, message: Message):
    """ вкл/выкл пересылки """
    global SEND
    if SEND:
        SEND = False
    else:
        SEND = True
    await message.reply(f"моментальная пересылка {'вкл' if SEND else 'выкл'}")


@app1.on_message(filters.chat(config.admins) & filters.command('set_posts'))
@app2.on_message(filters.chat(config.admins) & filters.command('set_posts'))
async def set_posts(client, message: Message):
    """ установить нужное количество постов для пересылки """
    global g
    try:
        set_number_posts(int(message.command[1]))
        await message.reply(f"Количество постов {get_number_posts()} установлено")
    except:
        await message.reply("Введите /set_posts число")
