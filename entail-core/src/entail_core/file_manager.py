import asyncio

from aiofile import async_open

from entail_core.async_dict import AsyncDict
from entail_core.constants import ENTAIL_FILE_EXTENSION


class FileManager:
    """Manages a set of files."""

    def __init__(self):
        self.files = AsyncDict()
        """Maps paths to file texts."""

    async def get_text(self, path):
        text = await self.files.get(path)

        if text is not None:
            return text

        return await self.files.set(path, self.load_from_filesystem(path))

    async def set_text(self, path, text):
        async def get_text():
            return text

        self.files.set(path, get_text())

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
