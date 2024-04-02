import asyncio
from collections import defaultdict

from pyrogram import Client

from bot.bot.to_admin import to_admin
from bot.utils.utils import Album


async def get_old_albums(app: Client, chat_id: int, amount: int, used: list = []) -> list[Album]:
    albums: defaultdict[str, Album] = defaultdict()
    await to_admin("Start getting messages ")
    async for message in app.get_chat_history(chat_id):
        try:
            media_group_id = message.media_group_id
            if media_group_id is None or int(media_group_id) in used:
                continue

            photo = await app.download_media(message, in_memory=True)

            if media_group_id not in albums:
                album = Album(photos=[photo], media_group_id=media_group_id,
                              caption=(message.caption or message.text or ""), chat_id=chat_id)
                albums[media_group_id] = album
            else:
                album = albums[media_group_id]
                album.caption = (message.caption or message.text or album.caption)
                album.photos.append(photo)
        except Exception as e:
            await to_admin(str(e))
            return []
        finally:
            await asyncio.sleep(0.02)
            if len(albums) == amount + 1:
                break
    await to_admin("Finished getting messages")
    return [albums[group_id] for group_id in albums if len(albums[group_id].photos) > 1]





