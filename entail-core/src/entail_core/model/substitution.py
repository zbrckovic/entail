import copy
from dataclasses import dataclass, field

from entail_core.model.formula.formula import Formula, AtomicFormula
from entail_core.model.formula.pred_vars_substitution_visitor import \
    SubstituteTemplate, SubstituteBecomesBoundException, \
    SubstituteBindsExternalIndVarException

Spec = tuple[AtomicFormula, Formula]


@dataclass
class Substitution:
    """Substitution of predicate variables performed on a theorem before it is
    applied inside the deduction."""

    theorem: Formula
    """Theorem on which substitution is being performed."""

    result: Formula
    """Resulting formula of the substitution."""

    specs: list[Spec] = field(default_factory=list)
    """Specifications of predicate variable substitutions which are performed 
    simultaneously."""

    def __post_init__(self):
        # Check that there is no predicate variable which occurs two times
        # among substitution specifications.

        # Maps predicate variables to the indexes of substitution
        # specifications in which they occur.
        pred_var_indexes = dict()

        for i, (atomic_f, _) in enumerate(self.specs):
            pred_var = atomic_f.pred_var

            indexes = pred_var_indexes.get(pred_var)
            if indexes is None:
                indexes = []
                pred_var_indexes[pred_var] = indexes

            indexes.append(i)

        # Find the first duplicate and raise an exception for it.
        for pred_var, indexes in pred_var_indexes.items():
            if len(indexes) > 1:
                raise DuplicatePredVarException(pred_var, indexes)

    def validate(self):
        formula = copy.copy(self.theorem)

        substitutions = {}
        for atomic_f, substitute_f in self.specs:
            substitute_template = SubstituteTemplate(substitute_f,
                                                     atomic_f.ind_vars)
            substitutions[atomic_f.pred_var] = substitute_template

        try:
            formula = formula.substitute_pred_vars(substitutions)
        except SubstituteBecomesBoundException as e:
            raise InvalidSubstitutionException(cause=e)
        except SubstituteBindsExternalIndVarException as e:
            raise InvalidSubstitutionException(cause=e)

        if formula != self.result:
            raise InvalidSubstitutionResultException(self.result, formula)


class DuplicatePredVarException(Exception):
    """When the same predicate variable is specified multiple times in the
    substitution."""

    def __init__(self, pred_var, indexes):
        self.pred_var = pred_var
        self.indexes = indexes
        super().__init__(
            f'predicate variable {pred_var} occurs multiple times at indexes: '
            f'{indexes}')


class InvalidSubstitutionException(Exception):
    def __init__(self, cause, index=None):
        self.cause = cause
        self.index = index
        """Index of the substitution inside the entail file."""

    def __str__(self):
        if isinstance(self.cause, SubstituteBecomesBoundException):
            return 'Substitute free individual variable becomes bound.'
        if isinstance(self.cause, SubstituteBindsExternalIndVarException):
            return 'Substitute binds external individual variable.'


class InvalidSubstitutionResultException(Exception):
    """When specified substitute result is not valid."""

    def __init__(self, formula, expected_formula, index=None):
        self.formula = formula
        self.expected_formula = expected_formula
        self.index = index
        super().__init__(f'Invalid substitution result. Expected '
                         f'{self.expected_formula}.')
