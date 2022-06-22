from entail_core.formula.constants import NEGATION, BICONDITIONAL, CONJUNCTION, \
    DISJUNCTION, CONDITIONAL, Quantifier
from entail_core.formula.formula import CompoundFormula, QuantifiedFormula


def is_conjunction(formula):
    return isinstance(formula, CompoundFormula) and \
           formula.operator == CONJUNCTION


def is_disjunction(formula):
    return isinstance(formula, CompoundFormula) and \
           formula.operator == DISJUNCTION


def is_conditional(formula):
    return isinstance(formula, CompoundFormula) and \
           formula.operator == CONDITIONAL


def is_biconditional(formula):
    return isinstance(formula, CompoundFormula) and \
           formula.operator == BICONDITIONAL


def is_negation(formula):
    return isinstance(formula, CompoundFormula) and \
           formula.operator == NEGATION


def is_negation_of(formula1, formula2):
    return is_negation(formula1) and formula1.formulas[0] == formula2


def is_conditional_of(formula, antecedent, consequent):
    return is_conditional(formula) and \
           formula.formulas == [antecedent, consequent]


def is_biconditional_of(formula, antecedent, consequent):
    return is_biconditional(formula) and \
           formula.formulas == [antecedent, consequent]


def is_universal(formula):
    return isinstance(formula, QuantifiedFormula) and \
           formula.quantifier == Quantifier.UNIVERSAL


def is_existential(formula):
    return isinstance(formula, QuantifiedFormula) and \
           formula.quantifier == Quantifier.EXISTENTIAL
