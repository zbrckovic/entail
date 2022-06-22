from unittest import TestCase

from entail_core.deduction.deduction import InvalidRuleApplicationException
from entail_core.deduction.rule import Rule
from .deduction_parser import DeductionParser


class TestDeduction(TestCase):
    def setUp(self):
        self.parser = DeductionParser()

    def test_a_out(self):
        deduction = self.parser.parse("""
            1) (x) A : PR;
            2) A : -A 1;
            """)
        deduction.validate()

        deduction = self.parser.parse("""
            1) (x) Fxy : PR;
            2) Fyy : -A 1;
            """)
        deduction.validate()

    def test_e_out(self):
        deduction = self.parser.parse("""
            1) [x] A : PR;
            2) A : -E 1;
            """)
        deduction.validate()

        deduction = self.parser.parse("""
            1) [x] Fxy : PR;
            2) Fyy : -E 1;
            """)
        deduction.validate()

    def test_if_in(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) A | B : +OR 1;
            3) A -> (A | B) : +IF;
            """)
        deduction.validate()

        deduction = self.parser.parse("""
            1) A : PR;
            2) A -> A : +IF;
            """)
        deduction.validate()

    def test_if_in_raises(self):
        deduction = self.parser.parse("""
           1) A : PR;
           2) A | B : +OR 1;
           3) A -> A : +IF;
           """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IF_IN.name):
            deduction.validate()

    def test_if_out(self):
        deduction = self.parser.parse("""
           1) A -> B : PR;
           2) A : PR;
           3) B : -IF 1, 2;
           """)
        deduction.validate()

    def test_if_out_raises(self):
        deduction = self.parser.parse("""
           1) A -> B : PR;
           2) A : PR;
           3) A : -IF 1, 2;
           """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IF_OUT.name):
            deduction.validate()

    def test_iff_in(self):
        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) B -> A : PR;
            3) A <-> B : +IFF 1, 2;
            """)
        deduction.validate()

    def test_iff_in_raises(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) B -> A : PR;
            3) A <-> B : +IFF 1, 2;
            """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) B & A : PR;
            3) A <-> B : +IFF 1, 2;
            """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) B -> B : PR;
            2) B -> A : PR;
            3) A <-> B : +IFF 1, 2;
            """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) B -> B : PR;
            3) A <-> B : +IFF 1, 2;
            """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) B -> A : PR;
            3) B <-> A : +IFF 1, 2;
            """)

        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_IN.name):
            deduction.validate()

    def test_iff_out(self):
        deduction = self.parser.parse("""
            1) A <-> B : PR;
            2) A -> B : -IFF 1;
            """)
        deduction.validate()

        self.assertEqual(deduction.lines[-1].rule_specific_data,
                         {'reversed': False})

    def test_iff_out_reversed(self):
        deduction = self.parser.parse("""
            1) A <-> B : PR;
            2) B -> A : -IFF 1;
            """)
        deduction.validate()

        self.assertEqual(deduction.lines[-1].rule_specific_data,
                         {'reversed': True})

    def test_iff_out_raises(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) A -> B : -IFF 1;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_OUT.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A <-> B : PR;
            2) A -> C : -IFF 1;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.IFF_OUT.name):
            deduction.validate()

    def test_and_in(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) B : PR;
            3) A & B : +AND 1, 2;
            """)
        deduction.validate()

    def test_and_in_raises(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) B : PR;
            3) B & A : +AND 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.AND_IN.name):
            deduction.validate()

    def test_and_out(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) A : -AND 1;
            """)
        deduction.validate()
        self.assertEqual(
            deduction.lines[-1].rule_specific_data,
            {'reverse': False})

    def test_and_out_reverse(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) B : -AND 1;
            """)
        deduction.validate()
        self.assertEqual(
            deduction.lines[-1].rule_specific_data,
            {'reverse': True})

    def test_and_out_raises(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) C : -AND 1;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.AND_OUT.name):
            deduction.validate()

    def test_or_in(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) A | B : +OR 1;
            """)
        deduction.validate()
        self.assertEqual(deduction.lines[-1].rule_specific_data,
                         {'reverse': False})

    def test_or_in_reverse(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) B | A : +OR 1;
            """)
        deduction.validate()
        self.assertEqual(deduction.lines[-1].rule_specific_data,
                         {'reverse': True})

    def test_or_in_raises(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) B | C : +OR 1;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.OR_IN.name):
            deduction.validate()

    def test_or_out(self):
        deduction = self.parser.parse("""
            1) A | B : PR;
            2) A -> C : PR;
            3) B -> C : PR;
            4) C : -OR 1, 2, 3;
            """)
        deduction.validate()

    def test_or_out_raises(self):
        deduction = self.parser.parse("""
            1) A | B : PR;
            2) A & C : PR;
            3) B -> C : PR;
            4) C : -OR 1, 2, 3;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.OR_OUT.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A | B : PR;
            2) A -> C : PR;
            3) B & C : PR;
            4) C : -OR 1, 2, 3;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.OR_OUT.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A | B : PR;
            2) A -> C : PR;
            3) B -> D : PR;
            4) C : -OR 1, 2, 3;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.OR_OUT.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A | B : PR;
            2) A -> C : PR;
            3) B -> C : PR;
            4) D : -OR 1, 2, 3;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.OR_OUT.name):
            deduction.validate()

    def test_not_in(self):
        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) A -> ~B : PR;
            3) ~A : +NOT 1, 2;
            """)
        deduction.validate()

    def test_not_in_raises(self):
        deduction = self.parser.parse("""
            1) A & B : PR;
            2) A -> ~B : PR;
            3) ~A : +NOT 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) A & ~B : PR;
            3) ~A : +NOT 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) B -> ~B : PR;
            3) ~A : +NOT 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) A -> ~A : PR;
            3) ~A : +NOT 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_IN.name):
            deduction.validate()

        deduction = self.parser.parse("""
            1) A -> B : PR;
            2) A -> ~B : PR;
            3) ~B : +NOT 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_IN.name):
            deduction.validate()

    def test_not_out(self):
        deduction = self.parser.parse("""
            1) ~~A : PR;
            2) A : -NOT 1;
            """)
        deduction.validate()

    def test_not_out_raises(self):
        deduction = self.parser.parse("""
            1) ~~A : PR;
            2) ~A : -NOT 1;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.NOT_OUT.name):
            deduction.validate()

    def test_explosion(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) ~A : PR;
            3) B : XP 1, 2;
            """)
        deduction.validate()

    def test_explosion_raises(self):
        deduction = self.parser.parse("""
            1) A : PR;
            2) ~~A : PR;
            3) B : XP 1, 2;
            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.EXPLOSION.name):
            deduction.validate()

    def test_repetition(self):
        deduction = self.parser.parse("""
                    1) A : PR;
                    2) A : RP 1;
                    """)
        deduction.validate()

    def test_repetition_raises(self):
        deduction = self.parser.parse("""
                            1) A : PR;
                            2) B : RP 1;
                            """)
        with self.assertRaisesRegex(InvalidRuleApplicationException,
                                    Rule.REPETITION.name):
            deduction.validate()
