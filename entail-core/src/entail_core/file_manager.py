import asyncio

from aiofile import async_open

from entail_core.constants import ENTAIL_FILE_EXTENSION


class FileManager:
    """Manages a set of files."""

    def __init__(self):
        self.tasks = {}
        """Maps paths to tasks which resolve to file texts if those files 
        are readable entail files."""

    def _set_task(self, path, task):
        old_task = self.tasks.get(path)

        if old_task is not None:
            old_task.cancel()

        self.tasks[path] = task

    async def get_text(self, path):
        task = self.tasks.get(path)

        if task is not None:
            return await task

        task = asyncio.create_task(self.load_from_filesystem(path))
        self.tasks[path] = task
        return await task

    async def set_text(self, path, text):
        async def get_text():
            return text

        task = asyncio.create_task(get_text())
        self._set_task(path, task)

    @staticmethod
    async def load_from_filesystem(path):
        if path.suffix != f'.{ENTAIL_FILE_EXTENSION}':
            raise InvalidExtensionException(path)

        if not path.is_file():
            raise NoSuchFileException(path)

        async with async_open(str(path)) as file:
            return await file.read()


class NoSuchFileException(Exception):
    def __init__(self, path):
        super().__init__(f'No such file "{path}".')
        self.path = path


class InvalidExtensionException(Exception):
    def __init__(self, path):
        super().__init__(f'File "{path}" doesn\'t have the required '
                         f'extension {ENTAIL_FILE_EXTENSION}.')
        self.path = path
