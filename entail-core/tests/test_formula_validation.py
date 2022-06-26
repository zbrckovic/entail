from unittest import TestCase

from entail_core.model.formula.constants import NEGATION, CONJUNCTION
from entail_core.model.formula.formula import AtomicFormula, CompoundFormula
from entail_core.model.formula.variables import PredVar, IndVar


class TestFormulaValidation(TestCase):
    """Tests that formula creation raises exception when provided with
    invalid parameters.
    """

    def test_raises_for_operator_arity(self):
        f = AtomicFormula(PredVar('F'))

        with self.assertRaises(ValueError):
            CompoundFormula(NEGATION, [f, f])

        with self.assertRaises(ValueError):
            CompoundFormula(CONJUNCTION, [f])

    def test_raises_for_predicate_arity(self):
        pred_var_0 = PredVar('F')  # nullary
        pred_var_1 = PredVar('G', 1)  # unary
        ind_var = IndVar('x')

        with self.assertRaisesRegex(ValueError, 'predicate arity'):
            AtomicFormula(pred_var_0, [ind_var])

        with self.assertRaisesRegex(ValueError, 'predicate arity'):
            AtomicFormula(pred_var_1)
