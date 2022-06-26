from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .constants import TFOperator, Quantifier
from .free_ind_var_substitution_finder_visitor import \
    FreeIndVarSubstitutionFinderVisitor
from .free_ind_vars_finder_visitor import FreeIndVarsFinderVisitor
from .free_ind_vars_substitution_visitor import FreeIndVarsSubstitutionVisitor
from .isomorphism_checking_visitor import IsomorphismCheckingVisitor
from .pred_vars_substitution_visitor import PredVarsSubstitutionVisitor
from .presentation_visitor import FormulaPresentationVisitor
from .variables import IndVar, PredVar


# Formula has `__hash__()` defined even-though it's mutable. This is fine as
# long as you don't mutate the formula and then count on the hash being the
# same. Sometimes we need to track formulas, and it's very practical to use
# them as dictionary keys or set elements. In such situations we just need to
# take care not to mutate formulas after they have been placed inside these
# collections.

@dataclass
class Formula(ABC):
    def __str__(self):
        visitor = FormulaPresentationVisitor()
        return visitor.visit(self)

    def find_free_ind_vars(self):
        """Finds all (distinct) free individual variables."""

        visitor = FreeIndVarsFinderVisitor()
        visitor.visit(self)
        return visitor.ind_vars

    def is_isomorphic_to(self, formula):
        """Checks whether two formulas are isomorphic - meaning they have the
        same structure regardless of specific choices of letters for their
        variables."""

        visitor = IsomorphismCheckingVisitor(self)
        try:
            return visitor.visit(formula)
        except ValueError:
            # Formulas don't have comparable structures.
            return False

    def substitute_free_ind_vars(self, substitutions):
        visitor = FreeIndVarsSubstitutionVisitor(substitutions)
        visitor.visit(self)

    def substitute_pred_vars(self, substitutions):
        visitor = PredVarsSubstitutionVisitor(substitutions)
        return visitor.visit(self)

    def contains_free(self, ind_var):
        return ind_var in self.find_free_ind_vars()

    def find_free_ind_var_substitution(self, formula):
        """Finds a substitution of free individual variable which would turn
        `self` into `formula`. If formulas are the same it returns `None` since
        no substitution is necessary. If formulas are not the same and such
        substitution is not possible, it raises a `ValueError`"""

        visitor = FreeIndVarSubstitutionFinderVisitor(self)
        visitor.visit(formula)
        return visitor.result

    @abstractmethod
    def accept(self, visitor):
        pass


@dataclass
class CompoundFormula(Formula):
    """Truth-functionally complex formula."""

    operator: TFOperator
    formulas: list[Formula] = field(default_factory=list)

    def __post_init__(self):
        if self.operator.arity != len(self.formulas):
            raise ValueError("operator arity and formulas count don't match")

    def accept(self, visitor):
        return visitor.visit_compound_formula(self)

    def __hash__(self):
        # Must be written manually because it has a mutable member (list).
        return hash((self.operator, tuple(self.formulas)))


@dataclass(unsafe_hash=True)
class QuantifiedFormula(Formula):
    quantifier: Quantifier

    ind_var: IndVar
    """The individual variable which is a part of `quantifier`.
    
    I will call this the "binding occurrence" of an individual variable. I will 
    use the phrase "bound occurrence" to refer to occurrence of an individual 
    variable in a predicate which is in the scope of a quantifier matching 
    "binding occurrence".
    """

    formula: Formula

    def accept(self, visitor):
        return visitor.visit_quantified_formula(self)

    def is_vacuous(self):
        return not self.formula.contains_free(self.ind_var)


@dataclass
class AtomicFormula(Formula):
    pred_var: PredVar
    ind_vars: list[IndVar] = field(default_factory=list)

    def __post_init__(self):
        if self.pred_var.arity != len(self.ind_vars):
            raise ValueError(
                "predicate arity and individual variables count don't match")

    def accept(self, visitor):
        return visitor.visit_atomic_formula(self)

    def __hash__(self):
        # Must be written manually because it has a mutable member (list).
        return hash((self.pred_var, tuple(self.ind_vars)))
