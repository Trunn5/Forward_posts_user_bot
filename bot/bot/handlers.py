from pyrogram import filters
from pyrogram.types import Message

from .. import config
from ..loader import bot, scheduler
from .. import globals
from ..sending import sending
from ..utils import is_valid_time_format


@bot.on_message(filters.chat(config.admins) & filters.command('set_posts'))
async def set_posts(client, message: Message):
    """ установить нужное количество постов для пересылки """
    try:
        globals.number_forwards_posts = int(message.command[1])
        await message.reply(f"Количество постов {globals.number_forwards_posts} установлено")
    except:
        await message.reply("Введите /set_posts число")


@bot.on_message(filters.chat(config.admins) & filters.command('switch'))
async def switch(client, message: Message):
    """ вкл/выкл пересылки """
    if globals.SEND:
        globals.SEND = False
    else:
        globals.SEND = True
    await message.reply(f"моментальная пересылка {'вкл' if globals.SEND else 'выкл'}")


@bot.on_message(filters.chat(config.admins) & filters.command('delete'))
async def delete(client, message: Message):
    """Удаление нового времени"""
    if len(message.command) < 2 or not is_valid_time_format(message.command[1]):
        await message.reply("Введите /add HH:MM")
        return
    time = message.command[1]
    if await scheduler.remove_task(sending, time):
        await message.reply(f"Успешно удалено время {time}")
    await current_tasks(client, message)


@bot.on_message(filters.chat(config.admins) & filters.command('add'))
async def add(client, message: Message):
    """Добавление нового времени"""
    if len(message.command) < 2 or not is_valid_time_format(message.command[1]):
        await message.reply("Введите /add HH:MM")
        return
    time = message.command[1]
    await scheduler.add_task(task=sending, run_time=time)
    await current_tasks(bot, message)


@bot.on_message(filters.chat(config.admins) & filters.command('current'))
async def current_tasks(client, message: Message):
    """Присылает текущие таймслоты на пересылку"""
    text = "Текущие расписание постов:\n" + '\n'.join([time for _, time, _ in scheduler.tasks])
    if len(scheduler.tasks) == 0: text += "Пусто"
    # print(message.text)
    await message.reply(text)


@bot.on_message(filters.user(config.admins) & filters.command("sbor"))
async def on_message(client, message: Message):
    await message.delete()
    with open(f"{message.chat.title}.txt", 'w') as f:
        print("Sbor userov s grupi: ", message.chat.title)
        async for member in message.chat.get_members():
            f.write(f"{member.user.username}\n")
