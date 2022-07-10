from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse


class ProjectManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    # TODO: Provide `deep` parameter. On each validation call remember the file
    #  uri and it's path for obtaining text from file manager. If `deep` is
    #  True, validate track imports recursively and populate the map of uris to
    #  valid loops.
    async def validate(self, path):
        text = await self.file_manager.get_text(path)
        print(text)
