from abc import ABC
from pathlib import Path

from entail_core.file_manager import FileManager


class EntailFileSummary(ABC):
    pass


class ProjectManager:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    # TODO: Provide `deep` parameter. On each validation call remember the file
    #  uri and it's path for obtaining text from file manager. If `deep` is
    #  True, validate track imports recursively and populate the map of uris to
    #  valid loops.
    async def validate(self, path: Path):
        text = await self.file_manager.get_text(path)

        print(text)
