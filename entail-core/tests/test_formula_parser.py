from unittest import TestCase

from entail_core.model.formula.constants import NEGATION, CONDITIONAL, Quantifier
from entail_core.model.formula.formula import AtomicFormula, CompoundFormula, \
    QuantifiedFormula
from entail_core.model.formula.variables import PredVar, IndVar
from entail_core.parser.formula_visitor import AmbiguousPredVarVisitedException
from .formula_parser import FormulaParser


class TestFormulaParser(TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_predicate_collision(self):
        self.parser.parse('Fx')

        with self.assertRaisesRegex(AmbiguousPredVarVisitedException,
                                    'found unequal predicate variables with '
                                    'the same id'):
            self.parser.parse('Fxy')

    def test_parser(self):
        for text, expected in self._create_cases():
            actual = self.parser.parse(text)
            self.assertEqual(actual, expected)

    @staticmethod
    def _create_cases():
        yield 'A', AtomicFormula(PredVar('A'))
        yield 'Fx', AtomicFormula(PredVar('F', 1), [IndVar('x')])
        yield 'F2xx', \
              AtomicFormula(PredVar('F2', 2), [IndVar('x'), IndVar('x')])
        yield 'F2xy', \
              AtomicFormula(PredVar('F2', 2), [IndVar('x'), IndVar('y')])
        yield '~A', \
              CompoundFormula(NEGATION, [AtomicFormula(PredVar('A'))])
        yield 'A -> B', \
              CompoundFormula(CONDITIONAL,
                              [AtomicFormula(PredVar('A')),
                               AtomicFormula(PredVar('B'))])
        yield '(x) Fx', \
              QuantifiedFormula(Quantifier.UNIVERSAL,
                                IndVar('x'),
                                AtomicFormula(PredVar('F', 1),
                                              [IndVar('x')]))
        yield '[x] Fx', \
              QuantifiedFormula(Quantifier.EXISTENTIAL,
                                IndVar('x'),
                                AtomicFormula(PredVar('F', 1),
                                              [IndVar('x')]))
