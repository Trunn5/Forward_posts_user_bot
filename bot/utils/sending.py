import asyncio

from pyrogram.errors import SlowmodeWait, ChatWriteForbidden, FloodWait
from pyrogram.types import InputMediaPhoto

from bot import config
from bot.bot.to_admin import to_admin
from bot.utils.utils import Album, DailyAlbums, check_stop_sign
from bot.scheduler.get_old_albums import get_old_albums
from bot.utils.loader import clientManager, bot

from db.connection import session, RentChannelForward, DefaultSpamValue, SellChannelForward, RentChannelSource, \
    SellChannelSource, Admin


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

    channel_from = (await clientManager.clients[0].get_chat(channel_id)).title

    text = f"Рассылка из {channel_from} в:\n"

    for group in groups:
        text += f"{group.title}\n"

    await to_admin(text)

    daily_albums = DailyAlbums()

    # Сбор старых сообщений
    while True:
        try:
            messages = await get_old_albums(clientManager.clients[0], channel_id, limit, daily_albums.get_todays_albums())
            break
        except FloodWait as e:
            await to_admin(f"Спам при сборе сообщений, жду {e} с.")
            await asyncio.sleep(e.value+0.01)

    for album in messages:
        # Первое фото с текстом
        media = [InputMediaPhoto(media=album.photos[0], caption=album.caption)]
        # Остальные фото без текста
        media += [InputMediaPhoto(media=photo) for photo in album.photos[1:]]
        for admin in session.query(Admin).all():
            while True:
                try:
                    await bot.send_message(text="Эти сообщения мне удалось собрать:", chat_id=admin.id)
                    await bot.send_media_group(media=media, chat_id=admin.id)
                    await asyncio.sleep(2)
                    break
                except FloodWait as e:
                    await asyncio.sleep(e.value)

    # Отметить сообщение, что они уже отправлены сегодня
    for message in messages:
        daily_albums += message.media_group_id

    default_delay_groups = [x.id for x in groups if x.interval is None]
    unique_delay_groups = [x for x in groups if x.interval is not None]

    default_spam_interval = session.query(DefaultSpamValue).first().value
    #async def cycle():
      #  for i in range(min(limit, len(messages))):
     #       try:
    #            await forward_post(messages[i], default_delay_groups)
   #             await asyncio.sleep(default_spam_interval)
  #          except Exception as e:
 #               await to_admin(e)
#        await to_admin("Рассылка с обычной задержкой окончена.")
    async def to_group(group, albums):
        for album in albums:
            await send_album(group, album)
            await asyncio.sleep(default_spam_interval)

    await asyncio.gather(*[to_group(group, messages[:limit]) for group in default_delay_groups])


async def send_album(chat_id: str | int, album: Album, user_bot_id: int = -1):
    """
    Пересылает альбом в чат.
    """
    # Первое фото с текстом
    media = [InputMediaPhoto(media=album.photos[0], caption=album.caption)]
    # Остальные фото без текста
    media += [InputMediaPhoto(media=photo) for photo in album.photos[1:]]

    # Разделение айди вида -100123123_123123.
    chat_id, reply_id = map(int, str(chat_id).split('_')) if '_' in chat_id else (chat_id, None)

    await to_admin(f"Отправляю альбом в чат {chat_id}, {reply_id}.\n{album.caption[:30]}...")

    # Если мы перебираем ботов и дошли до последнего, значит ни один из них
    # не может отпраить сообщение => завершаем
    if user_bot_id >= len(clientManager.clients):
        return

    if user_bot_id == -1:  # Если не перебираем ботов, то берем рабочего.
        client = clientManager.get_worker()
    else:                  # Иначе берем по списку.
        client = clientManager.clients[user_bot_id]
    try:
        # Отправляем альбом.
        await client.send_media_group(chat_id=int(chat_id), reply_to_message_id=reply_id, media=media)
    # Ошибка спама
    except FloodWait as e:
        await to_admin(f"Спам предупреждение, жду {e.value} с.")
        await asyncio.sleep(e.value)
        # Пытаемся отправить сообщение тем же ботом.
        await client.send_media_group(chat_id=int(chat_id), reply_to_message_id=reply_id, media=media)
    # Ошибка медленного режима отрпавки в чате
    except SlowmodeWait as e:
        await to_admin(f"Предупреждение о медленном режиме.\n"
                       f"Попытка с другим аккаунтом...")
        await send_album(chat_id, album)
    # Остальные ошибки (бан, ...)
    except Exception as e:
        await to_admin(f"⛔️<b>Ошибка:</b> {(await client.get_me()).username} не может отправить сообщене.\n💬Чат: {chat_id}\nТип: {e}\n"
                       f"Попытка с другим аккаунтом...")
        await send_album(chat_id, album, user_bot_id+1)


async def forward_post(album: Album, groups: list[int | str]):
    # === СТОП ЗНАК ===
    if check_stop_sign(album.caption):
        return
    # ===============================
    for i, spam_group in enumerate(groups):
        try:
            await send_album(spam_group, album)
            await asyncio.sleep(0.1)
        except Exception as e:
            await to_admin(e)


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