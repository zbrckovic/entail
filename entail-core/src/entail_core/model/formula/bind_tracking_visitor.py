from abc import ABC

from .formula_visitor import FormulaVisitor


class BindTrackingVisitor(FormulaVisitor, ABC):
    """A Visitor which tracks which variables are bound."""

    def __init__(self):
        self._bound_ind_vars = dict()
        """Keeps information about how many times each individual variable was 
        bound by ancestors.
        """

    def _register_binding(self, ind_var):
        num = self._bound_ind_vars.get(ind_var, 0)
        num += 1
        self._bound_ind_vars[ind_var] = num

    def _unregister_binding(self, ind_var):
        num = self._bound_ind_vars.get(ind_var)
        num -= 1
        if num > 0:
            self._bound_ind_vars[ind_var] = num
        else:
            del self._bound_ind_vars[ind_var]

    def _is_bound(self, ind_var):
        return ind_var in self._bound_ind_vars

    def visit_quantified_formula(self, formula):
        self._register_binding(formula.ind_var)
        result = self.visit(formula.formula)
        self._unregister_binding(formula.ind_var)
        return result
