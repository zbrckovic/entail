import asyncio
import os.path
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse, unquote

from entail_core.deduction.deduction import InvalidRuleApplicationException
from entail_core.entail_file import DuplicateFormulaDeclarationException, \
    FormulaDeclarationTargetType, FormulaDeclarationTarget
from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse
from entail_core.parser.util import get_tree_range
from entail_core.substitution import InvalidSubstitutionException, \
    InvalidSubstitutionResultException
from entail_core.text_document_exception import TextDocumentException, \
    RelatedErrorInfo

from theorems_manager import InvalidEntailFileException, NoSuchFileException, \
    InvalidTheoremException


@dataclass
class EntailFileManager:
    """Handles a single entail file."""

    def __init__(self, theorems_manager, uri, txt_doc):
        self.theorems_manager = theorems_manager
        """Each entail file manager has a reference to theorems manager which
        which contains an information about imported theorems and is required 
        to validate theorem imports."""

        self.uri = uri

        self.txt_doc = txt_doc
        self.parse_result = None
        self.entail_file = None
        self._task = None
        self.path, self.dir = self._parse_uri(uri)

    def update_text(self, changes):
        self.clear()
        self.txt_doc.apply_changes(changes)

    def clear(self):
        """Clears anything that relates to the current text document."""

        if self._task is not None:
            self._task.cancel()
        self.parse_result = None
        self.entail_file = None

    def process(self, listener):
        coro = self._process(listener)
        self._task = asyncio.create_task(coro)
        return self._task

    async def _process(self, listener):
        text = self.txt_doc.get_text()

        # Parse new text.
        self.parse_result = await self._parse(text)

        # Report eventual errors from parsing result.
        listener.on_parsed(self, self.parse_result.errors)
        if len(self.parse_result.errors) > 0:
            # Stop the process if there were errors.
            return

        try:
            # Process AST.
            self.entail_file = await self._process_ast(self.parse_result.tree)

            # Report successful AST processing.
            listener.on_processed_ast(self)
        except TextDocumentException as e:
            # Report error in AST processing and stop the process.
            listener.on_processed_ast(self, [e])
            return

        # At this point it is safe to update the theorem manager because
        # theorem for this path is known. This will prevent unneeded
        # reads from the disk.
        self.theorems_manager.set(self.path, self.entail_file.theorem)

        # Validate the model and report eventual errors.
        validation_errors = await self._validate()
        listener.on_validated(self, validation_errors)

        if validation_errors is not None and len(validation_errors) > 0:
            return

        errors = [error async for error in self._validate_imports()]
        listener.on_validated_imports(self, errors)

    @staticmethod
    async def _parse(text):
        return parse(text)

    @staticmethod
    async def _process_ast(ast):
        return process_ast(ast)

    async def _validate(self):
        try:
            self.entail_file.validate()
        except DuplicateFormulaDeclarationException as e:
            range_ = self.get_range_from_declaration_target(e.target)

            previous_range = self.get_range_from_declaration_target(
                e.previous_target)

            related_info = RelatedErrorInfo(
                previous_range,
                'Duplicate')

            return [TextDocumentException(str(e), range_, [related_info])]
        except InvalidRuleApplicationException as e:
            line = self.parse_result.tree.deduction().lines[e.line_index]
            range_ = get_tree_range(line)
            return [TextDocumentException(str(e), range_)]
        except InvalidSubstitutionException as e:
            substitution_ctx = self.parse_result.tree.substitutions[e.index]
            range_ = get_tree_range(substitution_ctx)
            return [TextDocumentException(str(e), range_)]
        except InvalidSubstitutionResultException as e:
            substitution_ctx = self.parse_result.tree.substitutions[e.index]
            range_ = get_tree_range(substitution_ctx.result)
            return [TextDocumentException(str(e), range_)]

    def get_range_from_declaration_target(self, declaration_target):
        match declaration_target.type:
            case FormulaDeclarationTargetType.IMPORT:
                ctx = self.parse_result.tree.theoremImports[
                    declaration_target.index]
            case FormulaDeclarationTargetType.SUBSTITUTION:
                ctx = self.parse_result.tree.substitutions[
                    declaration_target.index]
            case _:
                raise ValueError('unknown declaration target type')

        return get_tree_range(ctx)

    async def _validate_imports(self):
        for i, theorem_import in enumerate(self.entail_file.theorem_imports):
            path = self.dir / theorem_import.path
            path = path.resolve()

            try:
                theorem = await self.theorems_manager.get(path)

                if not theorem_import.theorem.is_isomorphic_to(theorem):
                    raise InvalidTheoremException(
                        f'Formula `{theorem_import.theorem}` is not a '
                        f'substitutional variant of `{theorem}`.',
                    )
            except (NoSuchFileException, InvalidEntailFileException,
                    InvalidTheoremException) as e:
                target = FormulaDeclarationTarget(
                    FormulaDeclarationTargetType.IMPORT,
                    i
                )
                range_ = self.get_range_from_declaration_target(target)
                yield TextDocumentException(str(e), range_)

    @staticmethod
    def _parse_uri(uri):
        unquoted_uri = unquote(uri)
        uri_parsed = urlparse(unquoted_uri)

        # removing leading extra slash
        path_corrected = uri_parsed.path[1:]

        path = Path(path_corrected)
        dir_str, filename = os.path.split(path_corrected)
        dir_ = Path(dir_str)
        return path, dir_


class ProcessingListener(ABC):
    @abstractmethod
    def on_parsed(self, file_manager, errors=None):
        pass

    @abstractmethod
    def on_processed_ast(self, file_manager, errors=None):
        pass

    @abstractmethod
    def on_validated(self, file_manager, errors=None):
        pass

    @abstractmethod
    def on_validated_imports(self, file_manager, errors=None):
        pass
