С сайта my.telegram.org/auth достаём айди и хеш аккаунтов.
Прописываем их в переменные окружения.

API_ID_1 = os.getenv("API_ID_1").
API_HASH_1 = os.getenv("API_HASH_1").
API_ID_2 = os.getenv("API_ID_2").
API_HASH_2 = os.getenv("API_HASH_2").

В config.py:
 - айди админов в admins
 - айди каналов по аренде и продаже
 - айди групп для пересылки
