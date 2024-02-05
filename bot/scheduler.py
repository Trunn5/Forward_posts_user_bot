import asyncio
import time
from typing import Callable, Awaitable, Coroutine


class AsyncScheduler:
    """
    Запускает, останавливает ассинхронные задачаи в заданное время
    """
    def __init__(self):
        self.tasks = []

    async def task_runner(self, task: Callable, run_time: str):
        """
        Запускает задачу, которая выполняет каждый день в заданный run_time
        :param task: await Функция
        :param run_time: строка "HH:MM"
        """
        while True:
            current_time = time.strftime("%H:%M", time.localtime())
            if current_time == run_time:
                await task()
            await asyncio.sleep(60)

    async def add_task(self, task, run_time):
        loop = asyncio.get_event_loop()
        task_instance = asyncio.create_task(self.task_runner(task, run_time))
        self.tasks.append((task, run_time, task_instance))

    async def remove_task(self, task, run_time) -> bool:
        for t, r_t, task_instance in self.tasks:
            if t == task and r_t == run_time:
                task_instance.cancel()
                self.tasks.remove((t, r_t, task_instance))
                return True
        return False


async def main():
    ...


if __name__ == '__main__':
    asyncio.run(main())
