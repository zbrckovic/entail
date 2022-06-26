from copy import copy
from dataclasses import dataclass, field

from .bind_tracking_visitor import BindTrackingVisitor
from .free_ind_vars_substitution_visitor import IndVarBecomesBoundException
from .variables import IndVar


class PredVarsSubstitutionVisitor(BindTrackingVisitor):
    """Substitutes occurrences or predicate variables.

    Finds all occurrences of predicate variable and substitutes them with a
    formula derived from the template.
    """

    def __init__(self, substitutions):
        super().__init__()
        self._substitutions = substitutions
        """All substitutions to be performed simultaneously.
        
        Key is a predicate variable, and value is the substitute template which
        will be used to instantiate a formula for each occurrence of the 
        predicate variable.
        """

    def visit_compound_formula(self, formula):
        for i, child in enumerate(formula.formulas):
            formula.formulas[i] = self.visit(child)
        return formula

    def visit_quantified_formula(self, formula):
        formula.formula = super().visit_quantified_formula(formula)
        return formula

    def visit_atomic_formula(self, formula):
        template = self._substitutions.get(formula.pred_var)

        if template is None:
            return formula

        self._validate_not_bound(template)

        try:
            return template.create_substitute(formula.ind_vars)
        except IndVarBecomesBoundException:
            raise SubstituteBindsExternalIndVarException()

    def _validate_not_bound(self, template):
        """Checks that free variables of the substitute would not get bound."""

        free_ind_vars = template.free_ind_vars
        if any(self._is_bound(ind_var) for ind_var in free_ind_vars):
            raise SubstituteBecomesBoundException()


@dataclass
class SubstituteTemplate:
    formula: 'Formula'
    placeholders: list[IndVar] = field(default_factory=list)

    def __post_init__(self):
        if len(self.placeholders) != len(set(self.placeholders)):
            raise ValueError('placeholder individual variables not unique')

        self.free_ind_vars = (
                self.formula.find_free_ind_vars() - set(self.placeholders))

    def create_substitute(self, ind_vars):
        """Substitutes all placeholders with specified individual variables.

        It instantiates the formula which can be used as a substitute for the
        predicate.

        :param ind_vars: Individual variables to substitute for placeholders in
        the specified order as they appear in an atomic formula being replaced.
        """

        substitute = copy(self.formula)
        substitutions = dict(zip(self.placeholders, ind_vars))
        substitute.substitute_free_ind_vars(substitutions)
        return substitute


class SubstituteBecomesBoundException(Exception):
    """When free variable of a substitute becomes bound."""
    pass


class SubstituteBindsExternalIndVarException(Exception):
    """When substitute binds an external individual variable."""
    pass
