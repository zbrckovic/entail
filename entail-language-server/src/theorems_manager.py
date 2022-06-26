import asyncio
from asyncio import Task

from aiofile import async_open
from entail_core.model.formula.formula import Formula
from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse
from entail_core.text.text_document_exception import TextDocumentException


class TheoremsManager:
    def __init__(self):
        self.theorems = {}

    def set(self, path, theorem):
        old = self.theorems.get(path)
        if isinstance(old, Task):
            old.cancel()

        self.theorems[path] = theorem

    async def get(self, path):
        theorem_or_task = self.theorems.get(path)

        if isinstance(theorem_or_task, Formula):
            return theorem_or_task

        if isinstance(theorem_or_task, Task):
            return await theorem_or_task

        # theorem_or_task is `None`
        coro = self.load_from_filesystem(path)
        task = asyncio.create_task(coro)
        self.theorems[path] = task
        return await task

    async def load_from_filesystem(self, path):
        if path.suffix is None:
            path = path.with_suffix('.entail')
        else:
            if path.suffix != '.entail':
                raise InvalidEntailFileException('Invalid file.')

        if not path.is_file():
            raise NoSuchFileException(path)

        async with async_open(str(path)) as file:
            text = await file.read()

        parse_result = await self._parse(text)
        if len(parse_result.errors) > 0:
            raise InvalidEntailFileException("File contains errors.")

        try:
            entail_file = await self._process_ast(parse_result.tree)
        except TextDocumentException as e:
            raise InvalidEntailFileException("File contains errors.")

        return entail_file.theorem

    @staticmethod
    async def _parse(text):
        return parse(text)

    @staticmethod
    async def _process_ast(ast):
        return process_ast(ast)


class NoSuchFileException(Exception):
    def __init__(self, path):
        super().__init__(f'No such file {path}')
        self.path = path


class InvalidEntailFileException(Exception):
    pass


class InvalidTheoremException(Exception):
    pass
