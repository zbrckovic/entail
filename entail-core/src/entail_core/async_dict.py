import asyncio


class AsyncDict:
    """A dictionary of async values.

    This dictionary internally holds a dictionary of async tasks. When setting
    a value, you provide a coroutine which will be turned into a task. When
    getting a value you get this task to await. When deleting a value or
    setting a value over some existing one, the task associated with that key
    will be cancelled."""

    def __init__(self):
        self._tasks = {}

    async def get(self, key):
        task = self._tasks.get(key)
        if task is not None:
            return await task

    def set(self, key, coro):
        self.delete(key)
        task = asyncio.create_task(coro)
        self._tasks[key] = task
        return task

    def delete(self, key):
        old_task = self._tasks.get(key)

        if old_task is not None:
            old_task.cancel()
            del self._tasks[key]
