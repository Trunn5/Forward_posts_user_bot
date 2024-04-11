from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.bot import start
from bot.bot.fsm import fsm, fsm_filter
from bot.utils.loader import bot_client, scheduler
from bot.utils.sending import sending
from bot.utils.utils import is_valid_time_format


@bot_client.on_message(filters.regex("🗓Расписание"))
async def schedule(client: Client, message: Message):
    """Обработчик кнпоки расписание,
    выводит текущие расписание,
    возможность добавить/удалить."""
    k = ReplyKeyboardMarkup(keyboard =[
                            [KeyboardButton("➕Добавить")],
                             [KeyboardButton("➖Удалить")],
                             [KeyboardButton("🔙Назад")]
                              ],
                            resize_keyboard=True)
    fsm[message.from_user.id] = "schedule"
    text = "Текущие расписание постов:\n" + '\n'.join([time for _, time, _ in scheduler.tasks])
    if len(scheduler.tasks) == 0: text += "Пусто"
    await message.reply(text, reply_markup=k)


@bot_client.on_message(filters.regex("➕Добавить") & fsm_filter("schedule"))
async def schedule_add(client: Client, message: Message):
    """Обработчик кнопки на добавление времени в расписание"""
    fsm[message.from_user.id] += "_add"
    await message.reply("Отправьте время (hh:mm).")


@bot_client.on_message(filters.text & fsm_filter("schedule_add"))
async def schedule_adding(client: Client, message: Message):
    """Добавление времени в расписание перессылки"""
    time = message.text
    if not is_valid_time_format(time):
        await message.reply("Введите HH:MM")
        return
    fsm[message.from_user.id] = ''
    await scheduler.add_task(task=sending, run_time=time)
    await message.reply(f"Время {time} добавлено в расписание.")
    await start(client, message)


@bot_client.on_message(filters.regex("➖Удалить") & fsm_filter("schedule"))
async def schedule_rm(client: Client, message: Message):
    """Обработчик кнопки на удаление времени из расписания"""
    fsm[message.from_user.id] += "_rm"
    await message.reply("Отправьте время (hh:mm).")


@bot_client.on_message(filters.text & fsm_filter("schedule_rm"))
async def schedule_rming(client: Client, message: Message):
    """Удаление времени из расписания"""
    time = message.text
    if not is_valid_time_format(time):
        await message.reply("Введите HH:MM")
        return
    if await scheduler.remove_task(sending, time):
        await message.reply(f"Успешно удалено время {time}")
    fsm[message.from_user.id] = ''
    await start()