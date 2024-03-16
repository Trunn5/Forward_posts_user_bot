import re

from pyrogram.types import Message


def is_valid_time_format(time_str):
    """Проверяют строку на формат HH:MM"""
    time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')
    return bool(time_pattern.match(time_str))



def check_stop_sign(message: Message):
    return "⛔️" in str(message.caption) or "⛔️" in str(message.text)

