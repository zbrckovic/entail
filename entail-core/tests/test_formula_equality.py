from unittest import TestCase

from entail_core.model.formula.constants import NEGATION, CONJUNCTION, DISJUNCTION, \
    Quantifier
from entail_core.model.formula.formula import AtomicFormula, CompoundFormula, \
    QuantifiedFormula
from entail_core.model.formula.variables import PredVar, IndVar


class TestFormulaEquality(TestCase):
    def test_equals(self):
        f1 = AtomicFormula(PredVar('A'))
        f2 = AtomicFormula(PredVar('A'))
        self.assertEqual(f1, f2)

        f1 = AtomicFormula(PredVar('A'))
        f2 = AtomicFormula(PredVar('B'))
        self.assertNotEqual(f1, f2)

        f1 = AtomicFormula(PredVar('F', 1), [IndVar('x')])
        f2 = AtomicFormula(PredVar('F', 1), [IndVar('x')])
        self.assertEqual(f1, f2)

        f1 = AtomicFormula(PredVar('F', 1), [IndVar('x')])
        f2 = AtomicFormula(PredVar('F', 1), [IndVar('y')])
        self.assertNotEqual(f1, f2)

        f1 = CompoundFormula(NEGATION, [AtomicFormula(PredVar('A'))])
        f2 = CompoundFormula(NEGATION, [AtomicFormula(PredVar('A'))])
        self.assertEqual(f1, f2)

        f1 = CompoundFormula(NEGATION, [AtomicFormula(PredVar('A'))])
        f2 = CompoundFormula(NEGATION, [AtomicFormula(PredVar('B'))])
        self.assertNotEqual(f1, f2)

        f1 = CompoundFormula(CONJUNCTION, [AtomicFormula(PredVar('A')),
                                           AtomicFormula(PredVar('B'))])
        f2 = CompoundFormula(CONJUNCTION, [AtomicFormula(PredVar('A')),
                                           AtomicFormula(PredVar('B'))])
        self.assertEqual(f1, f2)

        f1 = CompoundFormula(CONJUNCTION, [AtomicFormula(PredVar('A')),
                                           AtomicFormula(PredVar('B'))])
        f2 = CompoundFormula(CONJUNCTION, [AtomicFormula(PredVar('B')),
                                           AtomicFormula(PredVar('A'))])
        self.assertNotEqual(f1, f2)

        f1 = CompoundFormula(CONJUNCTION, [AtomicFormula(PredVar('A')),
                                           AtomicFormula(PredVar('B'))])
        f2 = CompoundFormula(DISJUNCTION, [AtomicFormula(PredVar('A')),
                                           AtomicFormula(PredVar('B'))])
        self.assertNotEqual(f1, f2)

        f1 = QuantifiedFormula(Quantifier.UNIVERSAL,
                               IndVar('x'),
                               AtomicFormula(PredVar('A')))
        f2 = QuantifiedFormula(Quantifier.UNIVERSAL,
                               IndVar('x'),
                               AtomicFormula(PredVar('A')))
        self.assertEqual(f1, f2)

        f1 = QuantifiedFormula(Quantifier.UNIVERSAL,
                               IndVar('x'),
                               AtomicFormula(PredVar('A')))
        f2 = QuantifiedFormula(Quantifier.UNIVERSAL,
                               IndVar('y'),
                               AtomicFormula(PredVar('A')))
        self.assertNotEqual(f1, f2)

        f1 = QuantifiedFormula(Quantifier.UNIVERSAL,
                               IndVar('x'),
                               AtomicFormula(PredVar('A')))
        f2 = QuantifiedFormula(Quantifier.EXISTENTIAL,
                               IndVar('x'),
                               AtomicFormula(PredVar('A')))
        self.assertNotEqual(f1, f2)
