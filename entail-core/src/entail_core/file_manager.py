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
        """Sets the text of file explicitly to be held in memory, so it won't
        be read from filesystem when its text is requested. This anticipates
        the needs of entail server which gets the text of the opened file from
        text editor's buffer, and it wants to use it instead of the text as is
        on the filesystem ."""

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


class InvalidExtensionException(Exception):
    """When file being read doesn't have a required extension."""

    def __init__(self, path):
        super().__init__(f'File "{path}" doesn\'t have the required '
                         f'extension {ENTAIL_FILE_EXTENSION}.')
        self.path = path


class NoSuchFileException(Exception):
    """When file is not found on the filesystem."""

    def __init__(self, path):
        super().__init__(f'No such file "{path}".')
        self.path = path
