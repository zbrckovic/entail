from unittest import TestCase

from .formula_parser import FormulaParser


class TestIsomorphism(TestCase):
    def setUp(self):
        self.parser = FormulaParser()

    def test_isomorphism(self):
        for text1, text2, are_isomorphic in self._create_cases():
            formula1 = self.parser.parse(text1)
            formula2 = self.parser.parse(text2)

            if are_isomorphic:
                self.assertTrue(formula1.is_isomorphic_to(formula2),
                                f'{text1} not isomorphic to {text2}')
                self.assertTrue(formula2.is_isomorphic_to(formula1),
                                f'{text2} not isomorphic to {text1}')
            else:
                self.assertFalse(formula1.is_isomorphic_to(formula2),
                                 f'{text1} isomorphic to {text2}')
                self.assertFalse(formula2.is_isomorphic_to(formula1),
                                 f'{text2} isomorphic to {text1}')

    @staticmethod
    def _create_cases():
        yield 'A', 'A', True
        yield 'A', 'B', True
        yield 'A', '~A', False
        yield 'A', '~B', False
        yield 'A -> ~B', 'B -> ~A', True
        yield 'A -> ~A', 'A -> ~B', False
        yield 'Fx', 'Gy', True
        yield 'F2xy', 'G2yx', True
        yield 'F2xy', 'F2xx', False
        yield '(x) Fx', '[x] Fx', False,
        yield '(x) [y] F2xy', '(y) [x] F2xy', False
        yield '(x) [y] F2xy', '(y) [x] G2yx', True
        yield '(x) [y] F2xy', '(y) [x] G2yx', True
        yield '(x) (F2xy & [x] Gx)', '(y) (F2yz & [z] Gz)', True
