import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from pyrogram.types import Message


def is_valid_time_format(time_str):
    """Проверяют строку на формат HH:MM"""
    time_pattern = re.compile(r'^[0-2][0-9]:[0-5][0-9]$')
    return bool(time_pattern.match(time_str))



def check_stop_sign(text: str):
    return "⛔️" in text

@dataclass
class Album:
    chat_id: int
    media_group_id: str
    photos: list
    caption: str

# contains date: list[media groups]
class DailyAlbums:
    """Contains information about media_groups that client already has sent."""
    todays_albums: defaultdict[str, list[int]] = defaultdict(list[int])

    def __iadd__(cls, x: int):
        cls.todays_albums[datetime.now().strftime('%d.%m.%Y')].append(x)
        return cls

    def __contains__(cls, x: int):
        return x in cls.todays_albums[datetime.now().strftime('%d.%m.%Y')]

    def get_todays_albums(cls):
        return cls.todays_albums[datetime.now().strftime('%d.%m.%Y')]
