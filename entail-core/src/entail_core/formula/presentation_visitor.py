from abc import ABC

from .constants import Quantifier
from .formula_visitor import FormulaVisitor


class FormulaPresentationVisitor(FormulaVisitor, ABC):
    """Creates a text presentation for a formula."""

    def __init__(self):
        super().__init__()

        # For tracking when it is at root, so it knows whether to omit external
        # parentheses.
        self._is_at_root = True

    def visit_compound_formula(self, formula):
        match formula.operator.arity:
            case 1:
                self._is_at_root = False
                child_txt = self.visit(formula.formulas[0])
                return f'{formula.operator}{child_txt}'
            case 2:
                must_omit_parentheses = self._is_at_root
                first, second = formula.formulas

                self._is_at_root = False
                first_txt = self.visit(first)
                second_txt = self.visit(second)

                result = f'{first_txt} {formula.operator} {second_txt}'
                if not must_omit_parentheses:
                    result = f'({result})'
                return result
            case _:
                raise ValueError('unsupported arity over 2')

    def visit_quantified_formula(self, formula):
        match formula.quantifier:
            case Quantifier.UNIVERSAL:
                prefix = f'({formula.ind_var})'
            case Quantifier.EXISTENTIAL:
                prefix = f'[{formula.ind_var}]'
            case _:
                raise ValueError('unknown quantifier')

        child_txt = self.visit(formula.formula)
        return f'{prefix} {child_txt}'

    def visit_atomic_formula(self, formula):
        ind_var_ids = (ind_var.id_ for ind_var in formula.ind_vars)

        if len(formula.ind_vars) > 1 and \
                any(len(ind_var.id_) > 1 for ind_var in formula.ind_vars):
            # Some individual variable is longer than one letter, so use the
            # use parentheses and a comma separator.
            ind_vars_txt = ', '.join(ind_var_ids)
            ind_vars_txt = '(' + ind_vars_txt + ')'
        else:
            # All individual variables are one letter long so use the shorter
            # notation.
            ind_vars_txt = ''.join(ind_var_ids)

        return f'{formula.pred_var}{ind_vars_txt}'
