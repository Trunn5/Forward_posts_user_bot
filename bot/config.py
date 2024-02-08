import os


API_ID_1 = os.getenv("API_ID_1")
API_HASH_1 = os.getenv("API_HASH_1")
API_ID_2 = os.getenv("API_ID_2")
API_HASH_2 = os.getenv("API_HASH_2")

admins: list[int] = []

# Интвервал спама постов (в секундах)
spam_interval = 10


# айди канала/группы берем из веб версии тг
# или с помощью @username_to_id_bot

# Канал по аренде
rent_channel_id = -1001617975958
# Канал по продаже
sell_channel_id = -1001763835669

# Группы для перессылки
groups_to_spam = [
]
