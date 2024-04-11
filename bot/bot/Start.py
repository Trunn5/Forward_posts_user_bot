from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.bot.fsm import fsm
from bot.utils.loader import bot_client


@bot_client.on_message(filters.command("start") | filters.regex("🔙Назад"))
async def start(client: Client, message: Message):
    """Обработчик команды старт, выводит кнопки меню"""
    fsm[message.from_user.id] = ''
    k = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton("🗓Расписание")],
                    [KeyboardButton("🏠Аренда"), KeyboardButton("💰Продажа")],
                    [KeyboardButton("🔗Источник"), KeyboardButton("👥Админы")],
                    [KeyboardButton("⏱Глобальный интервал")]],
                    resize_keyboard=True)
    await message.reply("Кнопки снизу", reply_markup=k)
