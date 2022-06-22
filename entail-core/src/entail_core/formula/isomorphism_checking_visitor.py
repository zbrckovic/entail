from bidict import bidict, DuplicationError

from .formula_comparing_visitor import FormulaComparingVisitor


class IsomorphismCheckingVisitor(FormulaComparingVisitor):
    """Checks whether two comparable formulas are isomorphic.

    If formulas are not comparable, it raises a `ValueError`.
    """

    def __init__(self, ref_formula):
        """
        :param ref_formula: The reference formula which will be checked for
            isomorphism against the visited formula. Isomorphism is a
            symmetric relation, so it is not important which formula is the
            reference formula and which is the visited.
        """
        super().__init__(ref_formula)

        self._var_map = bidict()
        """Bijection between reference formula variables and visited formula 
        variables.
        """

        self.var_map = bidict()
        """Bijection between reference formula variables and visited formula 
        variables.
        """

    def _register_mapping(self, ref_var, vis_var):
        prev_vis_var = self._var_map.get(ref_var, None)
        if prev_vis_var is not None and prev_vis_var != vis_var:
            raise ValueError(
                f'attempted to associate {ref_var} with {vis_var} while '
                f'{ref_var} has already been associated to {prev_vis_var}')
        self._var_map[ref_var] = vis_var

    def visit_quantified_formulas(self, formula, ref_formula):
        if ref_formula.quantifier != formula.quantifier:
            return False

        # reference individual variable
        ref_ind_var = ref_formula.ind_var

        # visited individual variable
        vis_ind_var = formula.ind_var

        # Delete previous mappings temporarily before visiting descendants
        # because the binding shadows those individual variables in both
        # formulas.
        prev_vis_ind_var = self._var_map.pop(ref_ind_var, None)
        prev_ref_ind_var = self._var_map.inverse.pop(vis_ind_var, None)

        try:
            # Add temporary mapping for current binding individual variable.
            self._register_mapping(ref_ind_var, formula.ind_var)

            self.stack.append(self._ref_formula.formula)
            if not self.visit(formula.formula):
                return False
            self.stack.pop()

            # Remove temporary mapping for current binding individual variable.
            del self._var_map[ref_ind_var]

            # Return previously deleted mappings.
            if prev_vis_ind_var is not None:
                self._register_mapping(ref_ind_var, prev_vis_ind_var)
            if prev_ref_ind_var is not None:
                self._register_mapping(prev_ref_ind_var, vis_ind_var)
        except (DuplicationError, ValueError):
            return False
        return True

    def visit_compound_formulas(self, formula, ref_formula):
        if ref_formula.operator != formula.operator:
            return False

        for i, child_formula in enumerate(formula.formulas):
            self.stack.append(ref_formula.formulas[i])
            if not self.visit(child_formula):
                return False
            self.stack.pop()

        return True

    def visit_atomic_formulas(self, formula, ref_formula):
        try:
            self._register_mapping(ref_formula.pred_var,
                                   formula.pred_var)

            pairs = zip(ref_formula.ind_vars, formula.ind_vars)
            for ref_ind_var, ind_var in pairs:
                self._register_mapping(ref_ind_var, ind_var)

            return True
        except (DuplicationError, ValueError):
            return False
