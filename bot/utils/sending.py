import asyncio

from pyrogram.errors import SlowmodeWait, ChatWriteForbidden
from pyrogram.types import InputMediaPhoto

from bot import config
from bot.bot.to_admin import to_admin
from bot.utils.utils import Album, DailyAlbums, check_stop_sign
from bot.scheduler.get_old_albums import get_old_albums
from bot.utils.loader import clientManager

from db.connection import session, RentChannelForward, DefaultSpamValue, SellChannelForward, RentChannelSource, \
    SellChannelSource


async def sending():
    """
    Функция для пересылки по расписанию.
    """
    await to_admin("Начинается рассылка")
    await asyncio.gather(
        # ПРОДАЖА
        forwards_to_chats(int(session.query(RentChannelSource).first().id),
                            session.query(RentChannelForward).all(),
                            6,),
        # АРЕНДА
        forwards_to_chats(int(session.query(SellChannelSource).first().id),
                            session.query(SellChannelForward).all(),
                            6, ))

async def forwards_to_chats(channel_id: int, groups: list[RentChannelForward | SellChannelForward], limit: int):
    """
    Пересылает count постов из channel_id в groups
    """
    if len(groups) == 0:
        return
    await to_admin(f"Рассылка из {channel_id} в {[x.id for x in groups]}")
    daily_albums = DailyAlbums()

    # getting old messages
    messages = await get_old_albums(clientManager.clients[0], channel_id, limit, daily_albums.get_todays_albums())

    # mark messages that it is done today
    for message in messages:
        daily_albums += message.media_group_id

    default_delay_groups = [x.id for x in groups if x.interval is None]
    unique_delay_groups = [x for x in groups if x.interval is not None]

    default_spam_interval = session.query(DefaultSpamValue).first().value
    async def cycle():
        for i in range(min(limit, len(messages))):
            try:
                await forward_post(messages[i], default_delay_groups)
                await asyncio.sleep(default_spam_interval)
            except Exception as e:
                await to_admin(e)
        await to_admin("Рассылка с обычной задержкой окончена.")

    await asyncio.gather(cycle(), forwards_to_chats_unique(messages, unique_delay_groups))


async def forward_post(album: Album, groups: list[int | str]):
    # === СТОП ЗНАК ===
    if check_stop_sign(album.caption):
        return
    # ===============================
    for i, spam_group in enumerate(groups):
        try:
            await send_album(spam_group, album)
        except Exception as e:
            await to_admin(e)


async def send_album(chat_id: str | int, album: Album):
    media = [InputMediaPhoto(media=album.photos[0], caption=album.caption)]
    # rest photos without caption
    media += [InputMediaPhoto(media=photo) for photo in album.photos[1:]]
    chat_id, reply_id = str(chat_id).split('_') if '_' in chat_id else chat_id, None

    try:
        bot = clientManager.get_worker()
        await bot.send_media_group(chat_id=int(chat_id), reply_to_message_id=reply_id, media=media)
        await asyncio.sleep(0.2)
        return 1
    except SlowmodeWait as e:
        await asyncio.sleep(e.value)
        await send_album(chat_id, album)
    except ChatWriteForbidden as e:
        await to_admin(f"⛔️<b>Ошибка:</b> Аккаунт {(await bot.get_me()).username} не может отправить сообщение."
                       f"\n💬<b>Чат:</b> {(await bot.get_chat(int(chat_id))).title}\n⚙️ Тип:\n{e}")
    except Exception as e:
        await to_admin(f"Ошибка!\n{e}")


async def forwards_to_chats_unique(messages: list[Album], groups: list[RentChannelForward | SellChannelForward]):
    time = 0
    done = [0] * len(groups)
    while True:
        sent = False
        for i, group in enumerate(groups):
            if done[i] < len(messages):
                sent = True
            if time % group.get_interval == 0:
                await send_album(chat_id=group.id, album=messages[done[i]])
                done[i] += 1
                sent = True
        await asyncio.sleep(1)
        time += 1

        if not sent:
            break
