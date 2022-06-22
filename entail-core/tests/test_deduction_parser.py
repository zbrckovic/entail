from unittest import TestCase

from entail_core.parser.ast_processing_exceptions import \
    UnexpectedLineNumberException, \
    DependencyLineNumberOutOfRangeException, \
    InvalidDependencyPremisesException, PremiseEliminationException
from .deduction_parser import DeductionParser


class TestFormulaParser(TestCase):
    def setUp(self):
        self.parser = DeductionParser()

    def test_unexpected_line_number(self):
        with self.assertRaises(UnexpectedLineNumberException):
            self.parser.parse("""
            1) A : PR;
            3) B : PR;
            """)

    def test_line_number_out_of_range(self):
        with self.assertRaises(DependencyLineNumberOutOfRangeException):
            self.parser.parse("""
            1) A : PR;
            2) B : PR;
            3) A & B : +AND 1, 3;
            """)

    def test_invalid_dependency_premises(self):
        with self.assertRaises(InvalidDependencyPremisesException):
            self.parser.parse("""
            1) A : PR;
            2) B : PR;
            3) A & B : +AND 1, 2;
            4) B -> (A & B) : +IF;
            5) B : RP 2;
            """)

    def test_premise_elimination_error(self):
        with self.assertRaises(PremiseEliminationException):
            self.parser.parse("""
            1) A : PR;
            2) A : RP 1;
            3) A -> A : +IF;
            4) A -> (A -> A) : +IF;
            """)
