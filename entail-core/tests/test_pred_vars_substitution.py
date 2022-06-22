import unittest

from entail_core.formula.pred_vars_substitution_visitor import \
    SubstituteTemplate, SubstituteBecomesBoundException, \
    SubstituteBindsExternalIndVarException
from .formula_parser import FormulaParser


class TestPredVarsSubstitution(unittest.TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_pred_vars_substitution(self):
        for formula, substitutions, expected in self._create_cases():
            formula = self.parser.parse(formula)
            substitutions = self._create_substitutions(substitutions)
            expected = self.parser.parse(expected)

            formula = formula.substitute_pred_vars(substitutions)

            self.assertEqual(formula,
                             expected,
                             f'{formula} is not equal to {expected}')

    @staticmethod
    def _create_cases():
        yield 'A', {}, 'A'
        yield 'A', {'A': 'B'}, 'B'
        yield 'A', {'A': 'A -> B'}, 'A -> B'
        yield 'A -> B', {'A': 'B', 'B': 'A'}, 'B -> A'
        yield 'Fx', {'Fx': 'A -> B'}, 'A -> B'
        yield 'Fx', {'Fy': 'Gy'}, 'Gx'
        yield 'F2xy', {'F2xy': 'F2yx'}, 'F2yx'
        yield 'F2xx', {'F2xy': 'G2yx'}, 'G2xx'
        yield '[x] (Fx -> Gx)', \
              {'Fy': 'A -> Gy',
               'Gx': 'Fx'}, \
              '[x] ((A -> Gx) -> Fx)'

    def test_invalid_cases_cannot_create_substitute(self):
        for formula, substitutions in \
                self._create_invalid_cases_cannot_create_substitute():
            formula = self.parser.parse(formula)
            substitutions = self._create_substitutions(substitutions)

            with self.assertRaises(SubstituteBindsExternalIndVarException):
                formula.substitute_pred_vars(substitutions)

    @staticmethod
    def _create_invalid_cases_cannot_create_substitute():
        yield 'Fx', {'Fy': '(x) Fy'}
        yield '(x) Fx', {'Fy': '(x) Fy'}

    def test_invalid_cases_substitute_becomes_bound(self):
        for formula, substitutions in \
                self._create_invalid_cases_substitute_becomes_bound():
            formula = self.parser.parse(formula)
            substitutions = self._create_substitutions(substitutions)

            with self.assertRaises(SubstituteBecomesBoundException):
                formula.substitute_pred_vars(substitutions)

    @staticmethod
    def _create_invalid_cases_substitute_becomes_bound():
        yield '[x] A', {'A': 'Fx'}
        yield '(y) F2yx', {'F2xz': 'G2xy'}

    def _create_substitutions(self, substitutions):
        result = {}
        for atomic_f, substitute_f in substitutions.items():
            atomic_f = self.parser.parse(atomic_f)
            substitute_f = self.parser.parse(substitute_f)
            substitute_template = SubstituteTemplate(substitute_f,
                                                     atomic_f.ind_vars)
            result[atomic_f.pred_var] = substitute_template
        return result
