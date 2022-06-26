from unittest import TestCase

from entail_core.model.formula.constants import Quantifier, NEGATION, CONJUNCTION, \
    DISJUNCTION, BICONDITIONAL, CONDITIONAL
from entail_core.model.formula.formula import AtomicFormula, QuantifiedFormula, \
    CompoundFormula
from entail_core.model.formula.variables import PredVar, IndVar


class TestFormula(TestCase):
    """Tests formula's __str__ method.e"""

    def test_atomic_formula_str(self):
        for formula, expected in self._create_atomic_formula_cases():
            actual = str(formula)
            self.assertEqual(actual, expected)

    @staticmethod
    def _create_atomic_formula_cases():
        f = AtomicFormula(PredVar('A'))
        yield f, 'A'

        f = AtomicFormula(PredVar('F', 1), [IndVar('x')])
        yield f, 'Fx'

        f = AtomicFormula(PredVar('F', 2), [IndVar('x'), IndVar('y')])
        yield f, 'Fxy'

        f = AtomicFormula(PredVar('F', 1), [IndVar('x1')])
        yield f, 'Fx1'

        f = AtomicFormula(PredVar('F', 2), [IndVar('x1'), IndVar('y')])
        yield f, 'F(x1, y)'

        f = AtomicFormula(PredVar('F', 2), [IndVar('x'), IndVar('y1')])
        yield f, 'F(x, y1)'

    def test_quantified_formula_str(self):
        for formula, expected in self._create_quantified_formula_cases():
            actual = str(formula)
            self.assertEqual(actual, expected)

    @staticmethod
    def _create_quantified_formula_cases():
        child_f = AtomicFormula(PredVar('A'))

        f = QuantifiedFormula(Quantifier.UNIVERSAL, IndVar('x'), child_f)
        yield f, '(x) A'

        f = QuantifiedFormula(Quantifier.EXISTENTIAL, IndVar('x'), child_f)
        yield f, '[x] A'

    def test_compound_formula_str(self):
        for formula, expected in self._create_compound_formula_cases():
            actual = str(formula)
            self.assertEqual(actual, expected)

    @staticmethod
    def _create_compound_formula_cases():
        child_f = AtomicFormula(PredVar('A'))

        f = CompoundFormula(NEGATION, [child_f])
        yield f, '~A'

        f = CompoundFormula(CONJUNCTION, [child_f, child_f])
        yield f, 'A & A'

        f = CompoundFormula(DISJUNCTION, [child_f, child_f])
        yield f, 'A | A'

        f = CompoundFormula(CONDITIONAL, [child_f, child_f])
        yield f, 'A -> A'

        f = CompoundFormula(BICONDITIONAL, [child_f, child_f])
        yield f, 'A <-> A'

        f = CompoundFormula(
            NEGATION,
            [CompoundFormula(CONJUNCTION, [child_f, child_f])])
        yield f, '~(A & A)'
