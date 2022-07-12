from abc import ABC, abstractmethod
from pathlib import Path


class TheoremsRetriever(ABC):
    """Returns theorem by a specified path."""

    @abstractmethod
    async def get(self, path: Path):
        pass


class NoSuchFileException(Exception):
    def __init__(self, path: Path):
        super().__init__(f'No such file {path}.')
        self.path = path


class InvalidEntailFileException(Exception):
    pass


class InvalidTheoremException(Exception):
    pass
