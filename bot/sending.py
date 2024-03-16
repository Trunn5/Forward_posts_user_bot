import asyncio
import re
import time
from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message, InputMedia, InputMediaPhoto

from bot import config
from bot.loader import app1, app2

from random import randint

from bot.utils import check_stop_sign
import globals


async def sending():
    """
    Функция для пересылки по расписанию.
    """
    await forwards_to_chats(config.rent_channel_id, config.groups_for_rent, globals.NUMBER_FORWARD_POSTS)
    # await forwards_to_chats(config.sell_channel_id, config.groups_for_sell, globals.NUMBER_FORWARD_POSTS)


# contains date: client: media groups
class DailyAlbums:
    """Contains information about media_groups that client already has sent."""
    todays_albums = list()

    def __iadd__(cls, x: tuple[Client, int]):
        s = f"{x[0].api_id}_{datetime.now().strftime('%d.%m.%Y')}_{x[1]}"
        cls.todays_albums.append(s)
        return cls

    def __contains__(cls, x: tuple[Client, int]):
        s = f"{x[0].api_id}_{datetime.now().strftime('%d.%m.%Y')}_{x[1]}"
        return s in cls.todays_albums


async def forwards_to_chats(channel_id: int, groups: list[int], limit: int):
    """
    Пересылает count постов из channel_id в groups
    """
    if len(groups) == 0:
        return
    daily_albums = DailyAlbums()
    messages = []
    messages2 = []

    # different instances of Message for clients
    async for post in app1.get_chat_history(chat_id=channel_id, limit=3000):
        if post.media_group_id and post.caption and (app1, post.media_group_id) not in daily_albums:
            messages += [post]
            daily_albums += (app1, post.media_group_id)
        if len(messages) == limit:
            break
        await asyncio.sleep(0.1)

    async for post in app2.get_chat_history(chat_id=channel_id, limit=3000):
        if post.media_group_id and post.caption and (app2, post.media_group_id) not in daily_albums:
            messages2 += [post]
            daily_albums += (app2, post.media_group_id)
        if len(messages2) == limit:
            break
        await asyncio.sleep(0.1)



    for i in range(min(limit, len(messages))):
        sent = False
        if (i%2==0 or not globals.IS_WORK_2) and globals.IS_WORK_1:
            await forward_post(app1, messages[i], groups)
            sent = True

        if not sent and globals.IS_WORK_2:
            await forward_post(app2, messages2[i], groups)



async def forward_post(client: Client, message: Message, groups: list[int, str]):
    # === СТОП ЗНАК ===
    if check_stop_sign(message) or not (message.caption or message.text):
        return
    # ===============================
    for i, spam_group in enumerate(groups):
        group_id, reply_id = (spam_group, None) if '_' not in str(spam_group) else list(
            map(int, str(spam_group).split('_')))
        # sleep for full sleep interval
        sleep_time = max(0, globals.spam_intervals[spam_group] - (time.time() - globals.spam_intervals[group_id]))
        await asyncio.sleep(sleep_time+0.1)
        try:
            if message.media_group_id:
                await client.copy_media_group(chat_id=group_id, from_chat_id=message.chat.id, message_id=message.id,
                                              reply_to_message_id=reply_id)
            else:
                await message.copy(group_id, reply_to_message_id=reply_id)
        except Exception as e:
            print(e)
            print(type(e))
