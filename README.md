## Настройка

Для использования данной конфигурации необходимо выполнить следующие шаги:

1. Загрузить зависимости requirements.txt
2. Получите API_ID, API_HASH для двух аккаунтов на https://my.telegram.org/auth.
3. Пропишите полученные значения в переменные окружения:

    config.py:
    ```python
    API_ID_1 = os.getenv("API_ID_1")
    API_HASH_1 = os.getenv("API_HASH_1")
    API_ID_2 = os.getenv("API_ID_2")
    API_HASH_2 = os.getenv("API_HASH_2")
    ```

4. В файле `config.py` укажите следующие данные:

    - `admins`: Идентификаторы администраторов.
    - `rent_channel_id, sell_channel_id`: Идентификаторы каналов для аренды и продажи.
    - `groups_to_spam`: Идентификаторы групп для пересылки.

## Запуск

Запуск файла main.py начнет работу ботов.
