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

admins: list[int] = []
