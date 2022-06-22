from unittest import TestCase

from entail_core.formula.variables import IndVar
from .formula_parser import FormulaParser


class TestFindFreeIndVarSubstitution(TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_find_free_ind_var_substitution(self):
        for text1, text2, expected_texts in self._create_cases():
            formula1 = self.parser.parse(text1)
            formula2 = self.parser.parse(text2)

            if expected_texts is None:
                expected = None
            else:
                ind_var_text_1, ind_var_text_2 = expected_texts
                ind_var_1 = IndVar(ind_var_text_1)
                ind_var_2 = IndVar(ind_var_text_2)
                expected = ind_var_1, ind_var_2

            diff = formula1.find_free_ind_var_substitution(formula2)
            self.assertEqual(expected, diff)

    @staticmethod
    def _create_cases():
        yield 'A', 'A', None
        yield 'Fx', 'Fx', None
        yield 'F2xy', 'F2xx', ('y', 'x')
        yield 'F2xx', 'F2yy', ('x', 'y')
        yield '(x) Fx', '(x) Fx', None
        yield '(z) F2xz -> [x] Gx', '(z) F2yz -> [x] Gx', ('x', 'y')
