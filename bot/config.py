import os
from dotenv import load_dotenv

load_dotenv()

api_ids = []
api_hashes = []

i = 1
while True:
    api_id = os.getenv(f"API_ID_{i}")
    api_hash = os.getenv(f"API_HASH_{i}")
    if api_id != None and api_hash != None:
        api_ids.append(api_id)
        api_hashes.append(api_hash)
        i += 1
    else:
        break

BOT_TOKEN = os.getenv("BOT_TOKEN")

admins: list[int] = [1503690284, 5899041406, 5501417707]

# Интвервал спама постов (в секундах)
spam_interval = 2


# айди канала/группы берем из веб версии тг
# или с помощью @username_to_id_bot

# Канал по аренде
rent_channel_id = -4198825337
# Канал по продаже
sell_channel_id = -4198825337

# Группы для перессылки
groups_for_rent = [-1001718089401] # -1001261922335, -1001588006106, -1001344216303, "-1001255272018_98960", "-1001910000434_1"]
groups_for_sell = [] # -1001261922335, -1001588006106, -1001344216303, "-1001255272018_98958"]

spam_intervals = {"-1001255272018_98958": 300, # 300 seconds = 5 minutes
                  -1001344216303: 20} # 20 seconds

# _albums: defaultdict[int, dict[str, Album]] = defaultdict(dict)

