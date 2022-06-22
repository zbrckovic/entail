from abc import ABC
from copy import copy

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.deduction.deduction import Rule, Line, Deduction
from entail_core.deduction.rule import rule_arities
from .ast_processing_exceptions import UnexpectedLineNumberException, \
    DependencyLineNumberOutOfRangeException, DuplicateDependencyException, \
    InvalidDependencyPremisesException, PremiseEliminationException, \
    RuleArityException
from .formula_visitor import FormulaVisitor


class DeductionVisitor(FormulaVisitor, ABC):
    """Handles parts of AST which represent a deduction.

    It raises exceptions for errors which can be immediately detected. This
    includes problems concerning line numbers, references to dependencies,
    premises, etc. Checks whether deduction is correct is made separately on
    the models constructed by this step. This separation is made so visitors
    can remain relatively fast.
    """

    def __init__(self, pred_vars=None):
        super().__init__(pred_vars)

        self.premises = list()
        """All premises which are currently in force.
        
        These are all premises which have been introduced in some previous
        line, but haven't been disposed yet."""

        self.lines = []

    @property
    def _current_line_number(self):
        return len(self.lines) + 1

    def visitDeduction(self, ctx):
        for line in ctx.lines:
            self.visit(line)

        return Deduction(self.lines)

    def visitLine(self, ctx):
        line_number = int(ctx.lineNumber.text)
        expected_line_number = self._current_line_number
        if line_number != expected_line_number:
            raise UnexpectedLineNumberException(ctx,
                                                line_number,
                                                expected_line_number)

        rule, dependencies = self.visit(ctx.ruleOfInference())
        formula = self.visit(ctx.rootFormula())

        line = Line(line_number,
                    formula,
                    rule,
                    dependencies,
                    copy(self.premises))
        self.lines.append(line)

    def visitRuleOfInference(self, ctx):
        rule = self._resolve_rule(ctx.ruleName)

        if rule is Rule.PREMISE:
            self.premises.append(self._current_line_number)
        if rule is Rule.IF_IN:
            try:
                self.premises.pop()
            except IndexError:
                raise PremiseEliminationException(ctx)

        if ctx.ruleDependencies() is not None:
            dependencies = list(
                self.visitRuleDependencies(ctx.ruleDependencies()))
        else:
            dependencies = []

        self._validate_arity(ctx, rule, dependencies)

        return rule, dependencies

    @staticmethod
    def _validate_arity(ctx, rule, dependencies):
        required_arity = rule_arities[rule]
        arity = len(dependencies)
        if arity != required_arity:
            raise RuleArityException(
                ctx,
                rule,
                arity,
                f'rule requires {required_arity} dependencies but got {arity}')

    def visitRuleDependencies(self, ctx):
        line_number_to_index_map = dict()

        for i, token in enumerate(ctx.lineNumbers):
            dependency_line_number = int(token.text)

            if dependency_line_number in line_number_to_index_map:
                raise DuplicateDependencyException(
                    ctx,
                    line_number_to_index_map[dependency_line_number],
                    i,
                    dependency_line_number)

            line_number_to_index_map[dependency_line_number] = i

            try:
                dependency_line = self.lines[dependency_line_number - 1]
            except IndexError:
                raise DependencyLineNumberOutOfRangeException(
                    ctx, i, dependency_line_number)

            # All premises which are in force at the dependency line must be
            # included in the set of premises which are in force at the current
            # line. This means that all dependencies for the current rule must
            # belong to the same branch of the deduction.
            dependency_premises = set(dependency_line.premises)
            premises = set(self.premises)
            if not dependency_premises.issubset(premises):
                raise InvalidDependencyPremisesException(
                    ctx,
                    self._current_line_number, premises,
                    dependency_line_number, dependency_premises)
            yield dependency_line_number

    @staticmethod
    def _resolve_rule(token):
        match token.type:
            case EntailLexer.RULE_PREMISE:
                return Rule.PREMISE
            case EntailLexer.RULE_THEOREM:
                return Rule.THEOREM
            case EntailLexer.RULE_A_IN:
                return Rule.A_IN
            case EntailLexer.RULE_A_OUT:
                return Rule.A_OUT
            case EntailLexer.RULE_E_IN:
                return Rule.E_IN
            case EntailLexer.RULE_E_OUT:
                return Rule.E_OUT
            case EntailLexer.RULE_IF_IN:
                return Rule.IF_IN
            case EntailLexer.RULE_IF_OUT:
                return Rule.IF_OUT
            case EntailLexer.RULE_IFF_IN:
                return Rule.IFF_IN
            case EntailLexer.RULE_IFF_OUT:
                return Rule.IFF_OUT
            case EntailLexer.RULE_AND_IN:
                return Rule.AND_IN
            case EntailLexer.RULE_AND_OUT:
                return Rule.AND_OUT
            case EntailLexer.RULE_OR_IN:
                return Rule.OR_IN
            case EntailLexer.RULE_OR_OUT:
                return Rule.OR_OUT
            case EntailLexer.RULE_NOT_IN:
                return Rule.NOT_IN
            case EntailLexer.RULE_NOT_OUT:
                return Rule.NOT_OUT
            case EntailLexer.RULE_EXPLOSION:
                return Rule.EXPLOSION
            case EntailLexer.RULE_REPETITION:
                return Rule.REPETITION
