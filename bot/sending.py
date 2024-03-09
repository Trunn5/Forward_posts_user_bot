import asyncio
import re
from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message, InputMedia, InputMediaPhoto

from bot import config
from bot.loader import app1, app2

from random import randint



daily_media_groups = set()
def get_daily():
    global daily_media_groups
    return daily_media_groups


def add_daily(group):
    global daily_media_groups
    daily_media_groups.add(group)


def clear_daily():
    global daily_media_groups
    daily_media_groups.clear()


NUMBER_POSTS = 6
def get_number_posts():
    global NUMBER_POSTS
    return NUMBER_POSTS

def set_number_posts(x: int):
    global NUMBER_POSTS
    NUMBER_POSTS = x




async def sending():
    """
    Функция для пересылки по расписанию.
    """
    await forwards_to_chats(config.rent_channel_id, config.groups_for_rent, get_number_posts())
    # await forwards_to_chats(config.sell_channel_id, config.groups_for_sell, get_number_posts())


async def forwards_to_chats(channel_id: int, groups: list[int], limit: int):
    """
    Пересылает count постов из channel_id в groups
    """
    if len(groups) == 0:
        return

    messages = []
    messages2 = []

    async for post in app1.get_chat_history(chat_id=channel_id, limit=2000):
        if (post.media_group_id and post.caption and not check_stop_sign(post)
                and (str(post.id) + str(post.media_group_id) + '.'+datetime.now().strftime("%d.%m.%Y")) not in get_daily()):
            messages += [post]
            add_daily(str(post.id) + str(post.media_group_id) + '.'+datetime.now().strftime("%d.%m.%Y"))
        if len(messages) == limit:
            break

    async for post in app2.get_chat_history(chat_id=channel_id, limit=2000):
        if post.media_group_id and post.caption and not check_stop_sign(
                post) and (str(post.id) + str(post.media_group_id) + '.'+datetime.now().strftime("%d.%m.%Y")) not in get_daily():
            messages2 += [post]
            add_daily(str(post.id) + str(post.media_group_id) + '.'+datetime.now().strftime("%d.%m.%Y"))
        if len(messages2) == limit:
            break

    for i in range(min(limit, len(messages))):
        if i % 2 == 0:
            await forward_post(app1, messages[i], groups)
        else:
            await forward_post(app2, messages2[i], groups)
        print(get_daily())
        await asyncio.sleep(config.spam_interval)


def is_valid_time_format(time_str):
    """Проверяют строку на формат HH:MM"""
    time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')
    return bool(time_pattern.match(time_str))


def check_stop_sign(message: Message):
    return "⛔️" in str(message.caption) or "⛔️" in str(message.text)


async def forward_post(client: Client, message: Message, groups: list[int, str]):
    # === СТОП ЗНАК ===
    if check_stop_sign(message) or not (message.caption or message.text):
        return
    # ===============================
    for spam_group in groups:
        group_id, reply_id = (spam_group, None) if '_' not in str(spam_group) else list(map(int, str(spam_group).split('_')))
        try:
            if message.media_group_id:
                await client.copy_media_group(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.id, reply_to_message_id=reply_id)
            else:
                await message.copy(group_id, reply_to_message_id=reply_id)
        except Exception as e:
            print(e)
            print(type(e))
        await asyncio.sleep(2)
