from pyrogram import filters
from pyrogram.types import Message

from bot import config
from bot.utils.loader import scheduler, bot_client, clientManager
from bot import globals
from bot.utils.sending import sending
from bot.utils.utils import is_valid_time_format


@bot_client.on_message(filters.user(config.admins) & filters.command('set_posts'))
async def set_posts(c, message: Message):
    """ установить нужное количество постов для пересылки """
    try:
        globals.NUMBER_FORWARD_POSTS = int(message.command[1])
        await message.reply(f"Количество постов {globals.NUMBER_FORWARD_POSTS} установлено")
    except:
        await message.reply("Введите /set_posts число")


@bot_client.on_message(filters.user(config.admins) & filters.command('switch'))
async def switch(c, message: Message):
    """ вкл/выкл пересылки """
    if globals.SEND:
        globals.SEND = False
    else:
        globals.SEND = True
    await message.reply(f"моментальная пересылка {'вкл' if globals.SEND else 'выкл'}")


@bot_client.on_message(filters.user(config.admins) & filters.command('delete'))
async def delete(c, message: Message):
    """Удаление нового времени"""
    time = message.text[8:]
    if not is_valid_time_format(time):
        await message.reply("Введите /add HH:MM")
        return
    if await scheduler.remove_task(sending, time):
        await message.reply(f"Успешно удалено время {time}")
    await current_tasks(c, message)



@bot_client.on_message(filters.user(config.admins) & filters.command('add'))
async def add(c, message: Message):
    """Добавление нового времени"""
    time = message.text[5:]
    if not is_valid_time_format(time):
        await message.reply("Введите /add HH:MM")
        return
    await scheduler.add_task(task=sending, run_time=time)
    await current_tasks(c, message)



@bot_client.on_message(filters.user(config.admins) & filters.command('current'))
async def current_tasks(client, message: Message):
    """Присылает текущие таймслоты на пересылку"""
    text = "Текущие расписание постов:\n" + '\n'.join([time for _, time, _ in scheduler.tasks])
    if len(scheduler.tasks) == 0: text += "Пусто"
    # print(message.text)
    await message.reply(text)


@bot_client.on_message(filters.user(config.admins) & filters.command('do_sleep'))
async def do_sleep(c, message: Message):
    try:
        clientManager.is_working[int(message.command[1]) - 1] = False
        await message.reply(f"Client {message.command[1]} is sleeping now")
    except Exception as e:
        await message.reply(e)


@bot_client.on_message(filters.user(config.admins) & filters.command('do_work'))
async def do_work(c, message: Message):
    try:
        clientManager.is_working[int(message.command[1]) - 1] = True
        await message.reply(f"Client {message.command[1]} is working now")
    except Exception as e:
        await message.reply(e)

