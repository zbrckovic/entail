from .bind_tracking_visitor import BindTrackingVisitor


class FreeIndVarsFinderVisitor(BindTrackingVisitor):
    """Finds all (distinct) free individual variables."""

    def __init__(self):
        super().__init__()
        self._ind_vars = set()
        """Visited free individual variables."""

    @property
    def ind_vars(self):
        return self._ind_vars

    def visit_compound_formula(self, formula):
        for child in formula.formulas:
            self.visit(child)

    def visit_atomic_formula(self, formula):
        for ind_var in formula.ind_vars:
            if not self._is_bound(ind_var):
                self._ind_vars.add(ind_var)
