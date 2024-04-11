import asyncio
import time

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaPhoto


class MyClient:
    action_interval = 10  # seconds
    last_action_time: float = 0
    is_working = True
    def __init__(self, client: Client):
        self.client = client

    async def needed_sleeping(self, action_time: float = action_interval):
        if time.time() - self.last_action_time < self.action_interval:
            await asyncio.sleep(self.last_action_time + self.action_interval - time.time())
        self.last_action_time = time.time()

    async def send_media_group(self,
                               chat_id: int,
                               media: list[InputMediaPhoto],
                               reply_to_message_id: int | None = None):
        await self.needed_sleeping()
        await self.client.send_media_group(chat_id=chat_id,
                                           media=media,
                                           reply_to_message_id=reply_to_message_id)

    async def send_message(self, chat_id: int, text: str, reply_to_message_id: int | None = None):
        await self.needed_sleeping(3)
        await self.client.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id)

    async def get_me(self):
        await self.needed_sleeping(1)
        return await self.client.get_me()

    async def get_chat(self, chat_id: int):
        await self.needed_sleeping(1)
        return await self.client.get_chat(chat_id)


class ClientManager:
    def __init__(self):
        self.clients: list[MyClient] = []
        self.last_worker_id = 0

    def add_client(self, client: Client):
        self.clients.append(MyClient(client))

    def get_worker(self):
        self.last_worker_id = (self.last_worker_id + 1) % len(self.clients)
        while not self.clients[self.last_worker_id].is_working:
            self.last_worker_id = (self.last_worker_id + 1) % len(self.clients)
        return self.clients[self.last_worker_id]

    def get_next_client(self, now: Client):
        for i, client in enumerate(self.clients):
            if client is now:
                return self.clients[(i + 1) % len(self.clients)]

    def sleep(self, worker: Client):
        for i, client in enumerate(self.clients):
            if client.client is worker:
                client.is_working = False

    def work(self, sleeper: Client):
        for i, client in enumerate(self.clients):
            if client.client is sleeper:
                client.is_working = True

    @property
    def numbers_clients(self):
        return len(self.clients)
