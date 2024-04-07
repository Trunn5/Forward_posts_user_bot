import asyncio
import traceback
from collections import defaultdict
from typing import Coroutine, TypeVar

from pyrogram import Client, filters
from pyrogram.types import Message

from bot import config
from bot.utils.loader import clientManager
from bot.utils.sending import forward_post
from bot.utils.utils import Album
from bot import globals
from db.connection import session, SellChannelForward, SellChannelSource, RentChannelSource, RentChannelForward

_tasks = set()
T = TypeVar("T")


def background(coro: Coroutine[None, None, T]) -> asyncio.Task[T]:
    loop = asyncio.get_event_loop()
    task = loop.create_task(coro)
    _tasks.add(task)
    task.add_done_callback(_tasks.remove)
    return task


# chat_id: group_id: album
_albums: defaultdict[int, dict[str, Album]] = defaultdict(dict)


@(clientManager.clients[0]).on_message(filters.media_group)
async def on_media_group(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        media_group_id = message.media_group_id
        if media_group_id is None:
            return


        if media_group_id not in _albums[chat_id]:
            album = Album(photos=[message], media_group_id=media_group_id,
                          caption=(message.caption or ""), chat_id=chat_id)
            _albums[chat_id][media_group_id] = album

            async def task():
                await asyncio.sleep(2)
                _albums[chat_id].pop(media_group_id, None)
                try:
                    await on_album(client, album)
                except Exception:
                    traceback.print_exc()

            background(task())
        else:
            album = _albums[chat_id][media_group_id]
            album.photos.append(message)
    finally:
        message.continue_propagation()


async def on_album(client: Client, album: Album):
    """
    Обрабатывает новые альбомы
    """
    if not globals.SEND:
        return

    for i, message in enumerate(album.photos):
        album.photos[i] = await client.download_media(message, in_memory=True)

    if str(album.chat_id) == session.query(SellChannelSource).first().id:
        await forward_post(album, [a.id for a in session.query(SellChannelForward).all()])
    elif str(album.chat_id) == session.query(RentChannelSource).first().id:
        await forward_post(album, [a.id for a in session.query(RentChannelForward).all()])
