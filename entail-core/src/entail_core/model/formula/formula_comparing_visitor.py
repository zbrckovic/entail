from abc import ABC, abstractmethod
from collections import deque

from .formula_visitor import FormulaVisitor


class FormulaComparingVisitor(FormulaVisitor, ABC):
    """Compares two formulas of comparable structures - the visited formula and
    the reference formula which the visited formula is compared against.

    Formulas have comparable structures if at each node of the tree their
    types match. If that's not the case, visitor will raise a `ValueError`.
    """

    def __init__(self, ref_formula):
        super().__init__()

        self.stack = deque((ref_formula,))
        """Tracks the current position inside the reference formula."""

    @property
    def _ref_formula(self):
        return self.stack[-1]

    def visit_compound_formula(self, formula):
        ref_formula = self._ref_formula

        if not isinstance(ref_formula, formula.__class__):
            raise ValueError("formulas don't have comparable structures")

        return self.visit_compound_formulas(formula, self._ref_formula)

    def visit_quantified_formula(self, formula):
        ref_formula = self._ref_formula

        if not isinstance(ref_formula, formula.__class__):
            raise ValueError("formulas don't have comparable structures")

        return self.visit_quantified_formulas(formula, self._ref_formula)

    def visit_atomic_formula(self, formula):
        ref_formula = self._ref_formula

        if not isinstance(ref_formula, formula.__class__):
            raise ValueError("formulas don't have comparable structures")

        return self.visit_atomic_formulas(formula, self._ref_formula)

    @abstractmethod
    def visit_compound_formulas(self, formula, ref_formula):
        pass

    @abstractmethod
    def visit_quantified_formulas(self, formula, ref_formula):
        pass

    @abstractmethod
    def visit_atomic_formulas(self, formula, ref_formula):
        pass
