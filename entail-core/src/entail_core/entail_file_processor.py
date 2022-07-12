from abc import abstractmethod, ABC
from pathlib import Path
from typing import AsyncGenerator

from entail_core.model.deduction.deduction import \
    InvalidRuleApplicationException
from entail_core.model.entail_file import EntailFile, \
    DuplicateFormulaDeclarationException, FormulaDeclarationTargetType, \
    FormulaDeclarationTarget
from entail_core.model.substitution import InvalidSubstitutionException, \
    InvalidSubstitutionResultException
from entail_core.parser.ast_processing import process_ast
from entail_core.parser.parsing import parse
from entail_core.parser.util import get_tree_range
from entail_core.text.text_document_exception import TextDocumentException, \
    RelatedErrorInfo
from entail_core.antlr.EntailParser import EntailParser
from entail_core.theorem_retriever import TheoremsRetriever, \
    InvalidTheoremException, NoSuchFileException, InvalidEntailFileException


class EntailFileProcessor:
    def __init__(self, theorems_repository: TheoremsRetriever):
        self.theorems_repository = theorems_repository

    async def process(
            self,
            path: Path,
            text: str,
            listener: 'ProcessingListener'):
        parse_result = await self._parse(text)
        if len(parse_result.errors) > 0:
            listener.on_parse_failed(parse_result.errors)
            return
        tree = parse_result.tree
        if not listener.on_parsed(tree):
            return

        try:
            entail_file = await self._process_ast(tree)
            if not listener.on_processed_ast(entail_file):
                return
        except TextDocumentException as e:
            listener.on_process_ast_failed(e)
            return

        validation_errors = await self._validate(tree, entail_file)
        if validation_errors is not None:
            listener.on_validate_failed(validation_errors)
            return
        if not listener.on_validated():
            return

        errors = [error async for error in
                  self._validate_imports(path, tree, entail_file)]
        if len(errors) > 0:
            listener.on_validate_imports_failed(errors)
            return
        listener.on_validated_imports()

    @staticmethod
    async def _parse(text: str):
        return parse(text)

    @staticmethod
    async def _process_ast(ast: EntailParser.StartContext):
        return process_ast(ast)

    async def _validate(self,
                        tree: EntailParser.StartContext,
                        entail_file: EntailFile):
        try:
            entail_file.validate()
        except DuplicateFormulaDeclarationException as e:
            range_ = self._get_range_from_declaration_target(tree, e.target)

            previous_range = self._get_range_from_declaration_target(
                tree,
                e.previous_target)

            related_info = RelatedErrorInfo(previous_range, 'Duplicate')

            return [TextDocumentException(str(e), range_, [related_info])]
        except InvalidRuleApplicationException as e:
            line = tree.deduction().lines[e.line_index]
            range_ = get_tree_range(line)
            return [TextDocumentException(str(e), range_)]
        except InvalidSubstitutionException as e:
            substitution_ctx = tree.substitutions[e.index]
            range_ = get_tree_range(substitution_ctx)
            return [TextDocumentException(str(e), range_)]
        except InvalidSubstitutionResultException as e:
            substitution_ctx = tree.substitutions[e.index]
            range_ = get_tree_range(substitution_ctx.result)
            return [TextDocumentException(str(e), range_)]

    async def _validate_imports(
            self,
            path: Path,
            tree: EntailParser.StartContext,
            entail_file: EntailFile
    ) -> AsyncGenerator[TextDocumentException, None]:
        for i, theorem_import in enumerate(entail_file.theorem_imports):
            path = path / theorem_import.path
            path = path.resolve()

            try:
                theorem = await self.theorems_repository.get(path)

                if not theorem_import.theorem.is_isomorphic_to(theorem):
                    raise InvalidTheoremException(
                        f'Formula `{theorem_import.theorem}` is not a '
                        f'substitutional variant of `{theorem}`.',
                    )
            except (
                    NoSuchFileException,
                    InvalidEntailFileException,
                    InvalidTheoremException) as e:
                target = FormulaDeclarationTarget(
                    FormulaDeclarationTargetType.IMPORT,
                    i
                )
                range_ = self._get_range_from_declaration_target(tree, target)
                yield TextDocumentException(str(e), range_)

    @staticmethod
    def _get_range_from_declaration_target(
            tree: EntailParser.StartContext,
            declaration_target: FormulaDeclarationTarget):
        match declaration_target.type:
            case FormulaDeclarationTargetType.IMPORT:
                ctx = tree.theoremImports[declaration_target.index]
            case FormulaDeclarationTargetType.SUBSTITUTION:
                ctx = tree.substitutions[declaration_target.index]
            case _:
                raise ValueError('unknown declaration target type')

        return get_tree_range(ctx)


class ProcessingListener(ABC):
    """
    Listens to entail file processing and signalizes with return values whether
    the processing should continue.
    """

    @abstractmethod
    def on_parsed(self, tree: EntailParser.StartContext) -> bool:
        pass

    @abstractmethod
    def on_parse_failed(self, errors: list[TextDocumentException]):
        pass

    @abstractmethod
    def on_processed_ast(self, entail_file_model: EntailFile) -> bool:
        pass

    @abstractmethod
    def on_process_ast_failed(self, error: TextDocumentException):
        pass

    @abstractmethod
    def on_validated(self) -> bool:
        pass

    @abstractmethod
    def on_validate_failed(self, errors: list[TextDocumentException]):
        pass

    @abstractmethod
    def on_validated_imports(self):
        pass

    @abstractmethod
    def on_validate_imports_failed(self, errors: list[TextDocumentException]):
        pass
