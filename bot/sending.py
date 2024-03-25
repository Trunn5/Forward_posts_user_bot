import asyncio
import datetime
import os
import re
import time
from collections import defaultdict
from datetime import datetime
from pprint import pprint

from pyrogram import Client
from pyrogram.errors import MediaEmpty, SlowmodeWait
from pyrogram.types import Message, InputMedia, InputMediaPhoto

from bot import config
from bot.bot.to_admin import to_admin
from bot.utils import Album, DailyAlbums
from bot.get_old_albums import get_old_albums
from bot.loader import bot, clientManager

from random import randint

from bot.utils import check_stop_sign
import bot.globals as globals


async def sending():
    """
    Функция для пересылки по расписанию.
    """
    print("start sending")
    await forwards_to_chats(config.rent_channel_id, config.groups_for_rent, globals.NUMBER_FORWARD_POSTS)
    # await forwards_to_chats(config.sell_channel_id, config.groups_for_sell, globals.NUMBER_FORWARD_POSTS)


async def forwards_to_chats(channel_id: int, groups: list[int], limit: int):
    """
    Пересылает count постов из channel_id в groups
    """
    if len(groups) == 0:
        return
    daily_albums = DailyAlbums()
    print(daily_albums.get_todays_albums())
    messages = await get_old_albums(clientManager.clients[0], channel_id, limit, daily_albums.get_todays_albums())
    for message in messages:
        daily_albums += message.media_group_id
    print('количество сообщений: ', len(messages))
    pprint(messages)
    for i in range(min(limit, len(messages))):
        client = clientManager.get_worker()
        await forward_post(client, messages[i], groups)
        print('pereslal ---')
    print("sending is done")
    await to_admin("Рассылка закончена")


async def forward_post(client: Client, album: Album, groups: list[int | str]):
    # === СТОП ЗНАК ===
    if check_stop_sign(album.caption):
        return
    # ===============================
    for i, spam_group in enumerate(groups):
        group_id, reply_id = (spam_group, None) if '_' not in str(spam_group) else list(
            map(int, str(spam_group).split('_')))
        # sleep for full sleep interval
        # sleep_time = max(0, globals.spam_intervals[spam_group] - (time.time() - globals.spam_intervals[group_id]))
        # await asyncio.sleep(sleep_time+0.1)

        # first photo with caption
        media = [InputMediaPhoto(media=album.photos[0], caption=album.caption)]
        # rest photos without caption
        media += [InputMediaPhoto(media=photo) for photo in album.photos[1:]]

        async def send(client: Client):
            try:
                await client.send_media_group(chat_id=group_id, reply_to_message_id=reply_id, media=media)
            except SlowmodeWait:
                await asyncio.sleep(1)
                await send(clientManager.get_worker())

        try:
            await send(client)
        except Exception as e:
            await to_admin(str(e))
            print('\n --- PROBLEM --- ')
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:"))
            print(type(e))
            print(e)
            print(' ^^^ problem ^^^ \n')
        finally:
            await asyncio.sleep(1)
