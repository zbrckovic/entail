from unittest import TestCase

from entail_core.formula.variables import IndVar
from .formula_parser import FormulaParser


class TestFreeIndVars(TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_find_free_ind_vars(self):
        for text, expected in self._create_cases():
            formula = self.parser.parse(text)
            actual = formula.find_free_ind_vars()
            self.assertEqual(actual, expected)

    @staticmethod
    def _create_cases():
        yield 'A', set()
        yield 'A -> ~B', set()
        yield 'Fx', {IndVar('x')}
        yield 'F2xx', {IndVar('x')}
        yield 'F2xy', {IndVar('x'), IndVar('y')}
        yield '(x) Fx', set()
        yield '(x) F2xx', set()
        yield '(x) F2xy', {IndVar('y')}
        yield '(x) [y] (F2xy -> ~G2yx)', set()
        yield '(x) (F2xy -> G2yx)', {IndVar('y')}
