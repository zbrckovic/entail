from .bind_tracking_visitor import BindTrackingVisitor


class FreeIndVarsSubstitutionVisitor(BindTrackingVisitor):
    """Substitutes occurrences of free individual variables.

    If the substitute individual variable would become bound it raises
    `IndVarBecomesBoundException`.
    """

    def __init__(self, substitutions):
        """
        :param substitutions: The dictionary which specifies substitutions.
            Key is an individual variable to replace, and the associated value
            is the substitute for that variable.
        """
        super().__init__()
        self._substitutions = substitutions

    def visit_compound_formula(self, formula):
        for child_formula in formula.formulas:
            self.visit(child_formula)

    def visit_atomic_formula(self, formula):
        for i, ind_var in enumerate(formula.ind_vars):
            if self._is_bound(ind_var):
                continue

            substitute = self._substitutions.get(ind_var)
            if substitute is None:
                continue
            if self._is_bound(substitute):
                raise IndVarBecomesBoundException()

            formula.ind_vars[i] = substitute


class IndVarBecomesBoundException(Exception):
    pass
