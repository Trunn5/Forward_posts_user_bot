С сайта my.telegram.org/auth достаём айди и хеш аккаунтов.\n
Прописываем их в переменные окружения.\n
API_ID_1 = os.getenv("API_ID_1")\n
API_HASH_1 = os.getenv("API_HASH_1")\n
API_ID_2 = os.getenv("API_ID_2")\n
API_HASH_2 = os.getenv("API_HASH_2")\n

В config.py:
 - айди админов в admins
 - айди каналов по аренде и продаже
 - айди групп для пересылки
