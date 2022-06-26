from .formula_comparing_visitor import FormulaComparingVisitor


class FreeIndVarSubstitutionFinderVisitor(FormulaComparingVisitor):
    """Compares formulas which differ only in one free individual variable
    in such a way that the visited formula can be obtained from the reference
    formula by substituting one free individual variable. It returns a pair of
    individual variables.

    If formulas differ in more than that, it raises a `ValueError`.
    """

    def __init__(self, ref_formula):
        """
        :param ref_formula: The reference formula which will be checked for
            against the visited formula.
        """
        super().__init__(ref_formula)

        self._bound_vars = set()

        self.free_ind_vars = set()
        """Free individual variables which are equal in both formulas."""

        self.ref_ind_var = None
        """Free individual variable in the reference formula which has been 
        substituted."""

        self.vis_ind_var = None
        """A substitute for `ref_ind_var` in the visited formula."""

    @property
    def result(self):
        if self.ref_ind_var is None:
            return None
        return self.ref_ind_var, self.vis_ind_var

    @property
    def _ref_formula(self):
        return self.stack[-1]

    def _register_free_ind_vars(self, ref_ind_var, vis_ind_var):
        if vis_ind_var in self._bound_vars:
            raise ValueError('substitute becomes bound')

        if ref_ind_var == vis_ind_var:
            # variable is the same in both formulas

            if self.ref_ind_var == ref_ind_var:
                # but it has been registered as a difference
                raise ValueError('substitution not total')

            self.free_ind_vars.add(ref_ind_var)
        else:
            # variables are different

            if ref_ind_var in self.free_ind_vars:
                raise ValueError('substitution not total')

            if self.ref_ind_var is None:
                # this is the first pair of different variables so far
                self.ref_ind_var = ref_ind_var
                self.vis_ind_var = vis_ind_var
            else:
                # some variable has already been registered
                if self.ref_ind_var != ref_ind_var:
                    raise ValueError('formulas differ in more than one free '
                                     'individual variable')

                if self.vis_ind_var != vis_ind_var:
                    raise ValueError('substitution not uniform')

    def visit_quantified_formulas(self, formula, ref_formula):
        if ref_formula.quantifier != formula.quantifier:
            raise ValueError('quantifiers not equal')

        # reference individual variable
        ref_ind_var = ref_formula.ind_var

        # visited individual variable
        vis_ind_var = formula.ind_var

        if ref_ind_var != vis_ind_var:
            raise ValueError('binding individual variables not equal')

        # whether there was already a quantifier higher up the tree which
        # binds the same variable (unusual case, but possible)
        was_bound_before = ref_ind_var in self._bound_vars
        if not was_bound_before:
            # adding the same thing two times to the set doesn't hurt, but it
            # doesn't help either.
            self._bound_vars.add(ref_ind_var)

        self.stack.append(self._ref_formula.formula)
        self.visit(formula.formula)
        self.stack.pop()

        if not was_bound_before:
            self._bound_vars.remove(ref_ind_var)

    def visit_compound_formulas(self, formula, ref_formula):
        if ref_formula.operator != formula.operator:
            raise ValueError('operators not equal')

        for i, child_formula in enumerate(formula.formulas):
            self.stack.append(ref_formula.formulas[i])
            self.visit(child_formula)
            self.stack.pop()

    def visit_atomic_formulas(self, formula, ref_formula):
        if ref_formula.pred_var != formula.pred_var:
            raise ValueError('predicate variables not equal')

        pairs = zip(ref_formula.ind_vars, formula.ind_vars)
        for ref_ind_var, ind_var in pairs:
            if ref_ind_var in self._bound_vars:
                if ref_ind_var != ind_var:
                    raise ValueError('bound individual variables not equal')
            else:
                self._register_free_ind_vars(ref_ind_var, ind_var)
