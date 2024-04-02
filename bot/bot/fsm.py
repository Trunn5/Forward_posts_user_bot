from collections import defaultdict

from pyrogram import filters

fsm: [int, str] = defaultdict(str)

def fsm_filter(data):
    async def fsm_func(flt, __, message):
        return fsm[message.from_user.id] == flt.data

    return filters.create(fsm_func, data=data)
