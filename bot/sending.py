import asyncio
import re

from bot import config
from bot.loader import app1, app2


async def sending():
    """
    Функция для пересылки по расписанию.
    """
    await forwards_to_chats(config.rent_channel_id, config.groups_to_spam, 20)
    await forwards_to_chats(config.sell_channel_id, config.groups_to_spam, 3)


async def forwards_to_chats(channel_id: int, groups: list[int], count: int):
    """
    Пересылает count постов из channel_id в groups
    """
    last_media_group_ids = set()
    limit = count
    async for post in app1.get_chat_history(chat_id=channel_id):
        if limit == 0:
            break
        if post.media_group_id in last_media_group_ids:
            await asyncio.sleep(.1)
            continue

        for spam_group in groups:
            if post.media_group_id:
                last_media_group_ids.add(post.media_group_id)
                if limit % 2 == 0:
                    mes = await app1.copy_media_group(chat_id=spam_group, from_chat_id=post.chat.id, message_id=post.id)
                else:
                    mes = await app2.copy_media_group(chat_id=spam_group, from_chat_id=post.chat.id, message_id=post.id)
            else:
                if limit % 2 == 0:
                    mes = await app1.copy_message(chat_id=spam_group, from_chat_id=post.chat.id, message_id=post.id)
                else:
                    mes = await app2.copy_message(chat_id=spam_group, from_chat_id=post.chat.id, message_id=post.id)
            await asyncio.sleep(1)
            # если сообщение успешно отослано, уменьшаем лимит
            if mes:
                limit -= 1


def is_valid_time_format(time_str):
    """Проверяют строку на формат HH:MM"""
    time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')
    return bool(time_pattern.match(time_str))
