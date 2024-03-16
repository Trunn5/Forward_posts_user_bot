import os
from dotenv import load_dotenv

load_dotenv()


API_ID_1 = os.getenv("API_ID_1")
API_HASH_1 = os.getenv("API_HASH_1")
API_ID_2 = os.getenv("API_ID_2")
API_HASH_2 = os.getenv("API_HASH_2")

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
