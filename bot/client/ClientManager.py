from pyrogram import Client


class ClientManager:
    def __init__(self):
        self.clients: list[Client] = []
        self.is_working: list[bool] = []
        self.last_worker_id = 0

    def add_client(self, client: Client):
        self.clients.append(client)
        self.is_working.append(True)

    def get_worker(self):
        self.last_worker_id = (self.last_worker_id + 1) % len(self.clients)
        while self.is_working[self.last_worker_id] == False:
            self.last_worker_id = (self.last_worker_id + 1) % len(self.clients)
        return self.clients[self.last_worker_id]

    def get_next_client(self, now: Client):
        for i, client in enumerate(self.clients):
            if client is now:
                return self.clients[(i + 1) % len(self.clients)]

    def sleep(self, worker: Client):
        for i, client in enumerate(self.clients):
            if client is worker:
                self.is_working[i] = False

    def work(self, sleeper: Client):
        for i, client in enumerate(self.clients):
            if client is sleeper:
                self.is_working[i] = True

    @property
    def numbers_clients(self):
        return len(self.clients)

