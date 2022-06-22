from dataclasses import dataclass

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.antlr.EntailVisitor import EntailVisitor
from entail_core.parser.util import is_inside_tree, is_inside_token, \
    get_token_range, \
    get_token_start_position, get_token_end_position, get_tree_range

from language_description import descriptions
from text.change import Range


def describe_position(tree, position):
    visitor = _DescriptionVisitor(position)
    visitor.visit(tree)
    return visitor.description


@dataclass
class Description:
    description: str
    range: Range


class _DescriptionVisitor(EntailVisitor):
    def __init__(self, position):
        self.position = position
        self.description = None

    def is_inside_tree(self, tree):
        return is_inside_tree(self.position, tree)

    def is_inside_token(self, token):
        return is_inside_token(self.position, token)

    def is_included_in(self, text_range):
        return text_range.includes(self.position)

    def visitTheoremImport(self, ctx):
        if self.is_inside_tree(ctx.theorem):
            theorem_range = get_tree_range(ctx.theorem)
            text = 'Theorem'
            self.description = Description(text, theorem_range)
        elif self.is_inside_token(ctx.filepath):
            text = 'Filepath'
            token_range = get_token_range(ctx.filepath)
            self.description = Description(text, token_range)

    def visitSubstitution(self, ctx):
        if self.is_inside_tree(ctx.theorem):
            theorem_range = get_tree_range(ctx.theorem)
            text = 'Theorem'
            self.description = Description(text, theorem_range)
            return

        for spec in ctx.specs:
            if self.is_inside_tree(spec):
                return self.visit(spec)

    def visitLine(self, ctx):
        if self.is_inside_tree(ctx.ruleOfInference()):
            return self.visit(ctx.ruleOfInference())

    def visitRuleOfInference(self, ctx):
        if self.is_inside_token(ctx.ruleName):
            token_range = get_token_range(ctx.ruleName)
            text = token_descriptions[ctx.ruleName.type]
            self.description = Description(text, token_range)

    def visitUniFormula(self, ctx):
        start = get_token_start_position(ctx.lParen)
        end = get_token_end_position(ctx.rParen)
        quantifier_range = Range(start, end)
        if quantifier_range.includes(self.position):
            text = 'Universal quantifier'
            self.description = Description(text, quantifier_range)
        else:
            return self.visit(ctx.formula())

    def visitExiFormula(self, ctx):
        start = get_token_start_position(ctx.lBracket)
        end = get_token_end_position(ctx.rBracket)
        quantifier_range = Range(start, end)
        if quantifier_range.includes(self.position):
            text = 'Existential quantifier'
            self.description = Description(text, quantifier_range)
        else:
            return self.visit(ctx.formula())

    def visitCompUnaryFormula(self, ctx):
        formula = ctx.formula()
        if is_inside_token(self.position, ctx.operator):
            text = token_descriptions[ctx.operator.type]
            token_range = get_token_range(ctx.operator)
            self.description = Description(text, token_range)
        elif is_inside_tree(self.position, formula):
            return self.visit(formula)

    def visitCompRootBinaryFormula(self, ctx):
        return self._visit_compound_binary_formula(ctx)

    def visitCompBinaryFormula(self, ctx):
        return self._visit_compound_binary_formula(ctx)

    def _visit_compound_binary_formula(self, ctx):
        if is_inside_tree(self.position, ctx.lFormula):
            return self.visit(ctx.lFormula)

        if is_inside_tree(self.position, ctx.binaryOperator()):
            binary_operator_token = self.visit(ctx.binaryOperator())
            text = token_descriptions[binary_operator_token.type]
            token_range = get_token_range(binary_operator_token)
            self.description = Description(text, token_range)
            return

        if is_inside_tree(self.position, ctx.rFormula):
            return self.visit(ctx.rFormula)

    def visitBinaryOperator(self, ctx):
        return ctx.operator

    def visitAtomicFormula(self, ctx):
        form_symbol_token = ctx.predVar

        if ctx.terms() is not None:
            term_symbol_tokens = self.visit(ctx.terms())
        else:
            term_symbol_tokens = []

        if is_inside_token(self.position, form_symbol_token):
            if len(term_symbol_tokens) > 0:
                text = 'Predicate'
            else:
                text = 'Proposition'
            token_range = get_token_range(form_symbol_token)
            self.description = Description(text, token_range)
        else:
            for term_symbol_token in term_symbol_tokens:
                if is_inside_token(self.position, term_symbol_token):
                    text = 'Term'
                    token_range = get_token_range(term_symbol_token)
                    self.description = Description(text, token_range)
                    return

    def visitTerms(self, ctx):
        return ctx.indVars


token_descriptions = dict([
    (EntailLexer.NEGATION, descriptions.negation),
    (EntailLexer.CONDITIONAL, descriptions.conditional),
    (EntailLexer.CONJUNCTION, descriptions.conjunction),
    (EntailLexer.DISJUNCTION, descriptions.disjunction),
    (EntailLexer.BICONDITIONAL, descriptions.biconditional),
    (EntailLexer.RULE_PREMISE, descriptions.rule_of_premise),
    (EntailLexer.RULE_THEOREM, descriptions.rule_of_theorem),
    (EntailLexer.RULE_A_IN, descriptions.rule_of_universal_generalization),
    (EntailLexer.RULE_A_OUT, descriptions.rule_of_universal_instantiation),
    (EntailLexer.RULE_E_IN, descriptions.rule_of_existential_generalization),
    (EntailLexer.RULE_E_OUT, descriptions.rule_of_existential_instantiation),
    (EntailLexer.RULE_IF_IN, descriptions.rule_of_deduction),
    (EntailLexer.RULE_IF_OUT, descriptions.rule_of_modus_ponens),
    (EntailLexer.RULE_IFF_IN, descriptions.rule_of_biconditional),
    (EntailLexer.RULE_IFF_OUT, descriptions.rule_of_converse_conditionals),
    (EntailLexer.RULE_AND_IN, descriptions.rule_of_conjunction),
    (EntailLexer.RULE_AND_OUT, descriptions.rule_of_simplification),
    (EntailLexer.RULE_OR_IN, descriptions.rule_of_addition),
    (EntailLexer.RULE_OR_OUT, descriptions.rule_of_dilemma),
    (EntailLexer.RULE_NOT_IN, descriptions.rule_of_reductio_ad_absurdum),
    (EntailLexer.RULE_NOT_OUT, descriptions.rule_of_double_negation),
    (EntailLexer.RULE_EXPLOSION, descriptions.rule_of_explosion),
])
