from unittest import TestCase

from entail_core.model.formula.free_ind_vars_substitution_visitor import \
    IndVarBecomesBoundException
from entail_core.model.formula.variables import IndVar
from .formula_parser import FormulaParser


class TestFreeIndVarsSubstitution(TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_free_ind_var_substitution(self):
        for formula, substitutions, expected in self._create_cases():
            formula = self.parser.parse(formula)
            expected = self.parser.parse(expected)
            substitutions = {IndVar(key): IndVar(value)
                             for key, value in substitutions.items()}
            formula.substitute_free_ind_vars(substitutions)
            self.assertEqual(formula, expected)

    @staticmethod
    def _create_cases():
        yield 'A', {}, 'A'
        yield 'Fx', {}, 'Fx'
        yield 'Fx', {'x': 'x'}, 'Fx'
        yield 'Fx', {'x': 'y'}, 'Fy'
        yield '(x) Fx', {'x': 'x'}, '(x) Fx'
        yield 'F2xx', {'x': 'y'}, 'F2yy'
        yield '(F2xy -> ~G2yx) & [x] F2yx', \
              {'x': 'y', 'y': 'z'}, \
              '(F2yz -> ~G2zy) & [x] F2zx'

    def test_invalid_free_ind_var_substitution(self):
        for formula, substitutions in self._create_invalid_cases():
            formula = self.parser.parse(formula)
            substitutions = {IndVar(key): IndVar(value)
                             for key, value in substitutions.items()}

            with self.assertRaises(IndVarBecomesBoundException):
                formula.substitute_free_ind_vars(substitutions)

    @staticmethod
    def _create_invalid_cases():
        yield '[x] F2xy', {'y': 'x'}
        yield '(x) [y] (F2xy -> ~Gz)', {'z': 'x'}
