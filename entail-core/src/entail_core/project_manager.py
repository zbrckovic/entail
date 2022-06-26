from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse


class ProjectManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    async def validate(self, path):
        text = await self.file_manager.get_text(path)
        print(text)
