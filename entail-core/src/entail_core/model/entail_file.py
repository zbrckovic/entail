from dataclasses import field, dataclass
from enum import Enum, auto

from entail_core.model.deduction.deduction import Deduction
from entail_core.model.formula.formula import Formula
from .substitution import Substitution, \
    InvalidSubstitutionException, InvalidSubstitutionResultException
from .theorem_import import TheoremImport


@dataclass
class EntailFile:
    deduction: Deduction
    theorem_imports: list[TheoremImport] = field(default_factory=list)
    substitutions: list[Substitution] = field(default_factory=list)

    theorem_declarations: dict[Formula, 'FormulaDeclarationTarget'] = field(
        default_factory=dict)
    """Maps each declared formula to the index of place of its declaration. 
    Will be initialized at validation."""

    @property
    def theorem(self):
        return self.deduction.theorem

    def validate(self):
        for i, theorem_import in enumerate(self.theorem_imports):
            declaration_target = FormulaDeclarationTarget(
                FormulaDeclarationTargetType.IMPORT, i)

            self._confirm_declaration_not_duplicate(
                theorem_import.theorem,
                declaration_target)

            theorem_import.validate()

        for i, substitution in enumerate(self.substitutions):
            declaration_target = FormulaDeclarationTarget(
                FormulaDeclarationTargetType.SUBSTITUTION, i)

            self._confirm_declaration_not_duplicate(
                substitution.result,
                declaration_target)

            try:
                substitution.validate()
            except InvalidSubstitutionException as e:
                e.index = i
                raise e
            except InvalidSubstitutionResultException as e:
                e.index = i
                raise e

        theorems = set(self.theorem_declarations.keys())

        self.deduction.validate(theorems)

    def _confirm_declaration_not_duplicate(self, theorem, current_target):
        previous_target = self.theorem_declarations.get(theorem)
        if previous_target is not None:
            raise DuplicateFormulaDeclarationException(
                theorem,
                current_target,
                previous_target)

        self.theorem_declarations[theorem] = current_target


class FormulaDeclarationTargetType(Enum):
    IMPORT = auto(),
    SUBSTITUTION = auto()


@dataclass
class FormulaDeclarationTarget:
    type: FormulaDeclarationTargetType
    index: int


@dataclass
class DuplicateFormulaDeclarationException(Exception):
    """When the same formula is declared multiple times."""

    def __init__(self, formula, target, previous_target):
        self.target = target
        self.previous_target = previous_target

        super().__init__(f'The same formula `{formula}` has been declared '
                         f'multiple times.')
