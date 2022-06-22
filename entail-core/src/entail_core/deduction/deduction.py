from dataclasses import dataclass, field

from .ind_var_dependency_graph import IndVarDependencyGraph, \
    CycleInducingDependencyException, \
    IndVarAlreadyRegisteredAsDependentException
from .line import Line
from .rule import Rule
from .utils import is_negation, is_negation_of, is_conditional, \
    is_disjunction, is_conjunction, is_biconditional, is_biconditional_of, \
    is_conditional_of, is_universal, is_existential


@dataclass
class Deduction:
    lines: list[Line]
    graph: IndVarDependencyGraph = field(default_factory=IndVarDependencyGraph)

    @property
    def theorem(self):
        return self.lines[-1].formula

    def update_graph(self, line_index, rule, dependent, dependencies):
        """Calculates new graph according to the changes required by the
        rule's individual variable dependencies. Also creates a second graph
        which contains removed individual variable dependencies and
        returns it as a result. Returns both graphs as a result."""

        removed = IndVarDependencyGraph()

        def on_remove(removed_dependent, removed_dependency):
            try:
                removed_dependencies = removed[removed_dependent]
            except KeyError:
                removed_dependencies = set()
                removed[removed_dependent] = removed_dependencies

            removed_dependencies.add(removed_dependency)

        try:
            self.graph.add_dependencies(dependent, dependencies, on_remove)
        except IndVarAlreadyRegisteredAsDependentException as e:
            raise InvalidRuleApplicationException(self, line_index, rule,
                                                  str(e))
        except CycleInducingDependencyException as e:
            raise InvalidRuleApplicationException(self, line_index, rule,
                                                  str(e))

        return removed

    def validate(self, theorems=None):
        if theorems is None:
            theorems = set()

        for i, line in enumerate(self.lines):
            dep_lines = [self.lines[d - 1] for d in line.dependencies]

            match line.rule:
                case Rule.PREMISE:
                    self.validate_premise(line, i)
                case Rule.THEOREM:
                    self.validate_theorem(line, i, theorems)
                case Rule.A_IN:
                    self.validate_a_in(line, i, dep_lines)
                case Rule.A_OUT:
                    self.validate_a_out(line, i, dep_lines)
                case Rule.E_IN:
                    self.validate_e_in(line, i, dep_lines)
                case Rule.E_OUT:
                    self.validate_e_out(line, i, dep_lines)
                case Rule.IF_IN:
                    self.validate_if_in(line, i, dep_lines)
                case Rule.IF_OUT:
                    self.validate_if_out(line, i, dep_lines)
                case Rule.IFF_IN:
                    self.validate_iff_in(line, i, dep_lines)
                case Rule.IFF_OUT:
                    self.validate_iff_out(line, i, dep_lines)
                case Rule.AND_IN:
                    self.validate_and_in(line, i, dep_lines)
                case Rule.AND_OUT:
                    self.validate_and_out(line, i, dep_lines)
                case Rule.OR_IN:
                    self.validate_or_in(line, i, dep_lines)
                case Rule.OR_OUT:
                    self.validate_or_out(line, i, dep_lines)
                case Rule.NOT_IN:
                    self.validate_not_in(line, i, dep_lines)
                case Rule.NOT_OUT:
                    self.validate_not_out(line, i, dep_lines)
                case Rule.EXPLOSION:
                    self.validate_explosion(line, i, dep_lines)
                case Rule.REPETITION:
                    self.validate_repetition(line, i, dep_lines)

    def validate_premise(self, line, line_index):
        pass

    def validate_theorem(self, line, line_index, theorems):
        res_formula = line.formula

        if res_formula not in theorems:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.THEOREM,
                'unknown theorem')

    def validate_a_in(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        res_formula = line.formula

        if not is_universal(res_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.A_IN,
                'resulting formula not universally quantified')

        try:
            substitution = dep_formula.find_free_ind_var_substitution(
                res_formula.formula
            )

            if substitution is None:
                # formulas are the same so quantification must be vacuous
                if not res_formula.is_vacuous():
                    raise ValueError
            else:
                ind_var, substitute_ind_var = substitution
                if not res_formula.ind_var == substitute_ind_var:
                    raise ValueError

                dependencies = dep_formula.find_free_ind_vars() - {ind_var}
                self.update_graph(line_index,
                                  Rule.A_IN,
                                  ind_var,
                                  dependencies)
        except ValueError:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.A_OUT,
                'resulting formula is not the result of universal '
                'generalization')

    def validate_a_out(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        res_formula = line.formula

        if not is_universal(dep_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.A_OUT,
                'dependency not universally quantified')

        try:
            substitution = dep_formula.formula.find_free_ind_var_substitution(
                res_formula
            )

            if substitution is None:
                # formulas are the same so quantification must be vacuous
                if not dep_formula.is_vacuous():
                    raise ValueError
            else:
                ind_var, _ = substitution
                if not dep_formula.ind_var == ind_var:
                    raise ValueError

        except ValueError:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.A_OUT,
                'resulting formula is not the result of universal '
                'instantiation')

    def validate_e_in(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        res_formula = line.formula

        if not is_existential(dep_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.E_IN,
                'resulting formula not existentially quantified')

        try:
            substitution = dep_formula.find_free_ind_var_substitution(
                res_formula.formula
            )

            if substitution is None:
                # formulas are the same so quantification must be vacuous
                if not res_formula.is_vacuous():
                    raise ValueError
            else:
                ind_var, substitute_ind_var = substitution
                if not res_formula.ind_var == substitute_ind_var:
                    raise ValueError
        except ValueError:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.A_OUT,
                'resulting formula is not the result of existential '
                'generalization')

    def validate_e_out(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        if not is_existential(dep_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.E_OUT,
                'dependency not existentially quantified')

        res_formula = line.formula

        try:
            substitution = dep_formula.formula.find_free_ind_var_substitution(
                res_formula
            )

            if substitution is None:
                # formulas are the same so quantification must be vacuous
                if not dep_formula.is_vacuous():
                    raise ValueError
            else:
                ind_var, substitute_ind_var = substitution
                if not dep_formula.ind_var == ind_var:
                    raise ValueError

                dependencies = res_formula.find_free_ind_vars() - {
                    substitute_ind_var}
                self.update_graph(line_index,
                                  Rule.E_OUT,
                                  substitute_ind_var,
                                  dependencies)
        except ValueError:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.E_OUT,
                'resulting formula is not the result of existential '
                'instantiation')

    def validate_if_in(self, line, line_index, dependencies):
        prev_line = self.lines[line_index - 1]
        premise_line_number = prev_line.premises[-1]
        premise = self.lines[premise_line_number - 1].formula
        consequent = prev_line.formula
        res_formula = line.formula

        if not is_conditional_of(res_formula, premise, consequent):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.IF_IN,
                'resulting formula not a conditional of premise and formula '
                'from the previous line')

    def validate_if_out(self, line, line_index, dependencies):
        dep1, dep2 = dependencies
        dep_formula1 = dep1.formula
        dep_formula2 = dep2.formula
        res_formula = line.formula

        if not is_conditional_of(dep_formula1, dep_formula2, res_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.IF_OUT,
                'first dependency formula is not a conditional of '
                'second dependency formula and resulting formula')

    def validate_iff_in(self, line, line_index, dependencies):
        dep1, dep2 = dependencies
        dep_formula1 = dep1.formula
        dep_formula2 = dep2.formula

        if not is_conditional(dep_formula1):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.IFF_IN,
                                                  'first dependency not conditional')

        if not is_conditional(dep_formula2):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.IFF_IN,
                                                  'second dependency not conditional')

        antecedent1, consequent1 = dep_formula1.formulas
        antecedent2, consequent2 = dep_formula2.formulas

        if antecedent1 != consequent2 or antecedent2 != consequent1:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.IFF_IN,
                'dependencies not converse conditionals')

        res_formula = line.formula

        if not is_biconditional_of(res_formula, antecedent1, consequent1):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.IFF_IN,
                'resulting formula not biconditional whose operands match '
                'first dependency')

    def validate_iff_out(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula

        if not is_biconditional(dep_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.IFF_OUT,
                'dependency not biconditional')

        res_formula = line.formula

        if not is_conditional(res_formula):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.IFF_OUT,
                                                  'resulting formula not conditional')

        if dep_formula.formulas == res_formula.formulas:
            line.rule_specific_data = {'reversed': False}
            return

        if dep_formula.formulas == list(reversed(res_formula.formulas)):
            line.rule_specific_data = {'reversed': True}
            return

        raise InvalidRuleApplicationException(
            self, line_index, Rule.IFF_OUT,
            'resulting antecedent and consequent not conditional')

    def validate_and_in(self, line, line_index, dependencies):
        res_formula = line.formula
        if not is_conjunction(res_formula):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.AND_IN,
                                                  'resulting formula not conjunction')

        dep1, dep2 = dependencies
        conjunct1, conjunct2 = res_formula.formulas

        if conjunct1 != dep1.formula or conjunct2 != dep2.formula:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.AND_IN,
                "resulting conjuncts don't match dependencies")

    def validate_and_out(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        if not is_conjunction(dep_formula):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.AND_OUT,
                                                  'dependency not conjunction')

        conjunct1, conjunct2 = dep_formula.formulas
        resulting_formula = line.formula

        if conjunct1 == resulting_formula:
            line.rule_specific_data = {'reverse': False}
            return

        if conjunct2 == resulting_formula:
            line.rule_specific_data = {'reverse': True}
            return

        raise InvalidRuleApplicationException(self, line_index, Rule.AND_OUT,
                                              'resulting formula not conjunct')

    def validate_or_in(self, line, line_index, dependencies):
        res_formula = line.formula
        if not is_disjunction(res_formula):
            raise InvalidRuleApplicationException(self, line_index, Rule.OR_IN,
                                                  'result not disjunction')

        dep_formula = dependencies[0].formula
        disjunct1, disjunct2 = res_formula.formulas

        if dep_formula == disjunct1:
            line.rule_specific_data = {'reverse': False}
            return

        if dep_formula == disjunct2:
            line.rule_specific_data = {'reverse': True}
            return

        raise InvalidRuleApplicationException(
            self, line_index, Rule.OR_IN,
            "neither of resulting disjuncts matches dependency")

    def validate_or_out(self, line, line_index, dependencies):
        dep1, dep2, dep3 = dependencies
        dep_formula1 = dep1.formula
        dep_formula2 = dep2.formula
        dep_formula3 = dep3.formula

        if not is_disjunction(dep_formula1):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.OR_OUT,
                                                  'first dependency not disjunction')

        if not is_conditional(dep_formula2):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.OR_OUT,
                                                  'second dependency not conditional')

        if not is_conditional(dep_formula3):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.OR_OUT,
                                                  'third dependency not conditional')

        consequent1 = dep_formula2.formulas[1]
        consequent2 = dep_formula3.formulas[1]

        if not consequent1 == consequent2:
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.OR_OUT,
                                                  'consequents not equal')

        res_formula = line.formula

        if res_formula != consequent1:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.OR_OUT,
                "resulting formula doesn't match consequents")

    def validate_not_in(self, line, line_index, dependencies):
        dep1, dep2 = dependencies
        dep_formula1 = dep1.formula
        dep_formula2 = dep2.formula

        if not is_conditional(dep_formula1):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.NOT_IN,
                                                  'first dependency not conditional')

        if not is_conditional(dep_formula2):
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.NOT_IN,
                                                  'second dependency not conditional')

        antecedent1, consequent1 = dep_formula1.formulas
        antecedent2, consequent2 = dep_formula2.formulas

        if antecedent1 != antecedent2:
            raise InvalidRuleApplicationException(self, line_index,
                                                  Rule.NOT_IN,
                                                  "antecedents don't match")

        if not is_negation_of(consequent2, consequent1):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.NOT_IN,
                "second consequent not negation of first one")

        res_formula = line.formula

        if not is_negation_of(res_formula, antecedent1):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.NOT_IN,
                "resulting formula not negation of antecedent")

    def validate_not_out(self, line, line_index, dependencies):
        res_formula = line.formula
        dep_formula = dependencies[0].formula
        if not is_negation(dep_formula) or \
                not is_negation_of(dep_formula.formulas[0], res_formula):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.NOT_OUT,
                "dependency not double negation of resulting formula")

    def validate_explosion(self, line, line_index, dependencies):
        dep1, dep2 = dependencies
        dep_formula1 = dep1.formula
        dep_formula2 = dep2.formula

        if not is_negation_of(dep_formula2, dep_formula1):
            raise InvalidRuleApplicationException(
                self, line_index, Rule.EXPLOSION,
                "second dependency not negation of first one")

    def validate_repetition(self, line, line_index, dependencies):
        dep_formula = dependencies[0].formula
        res_formula = line.formula

        if not dep_formula == res_formula:
            raise InvalidRuleApplicationException(
                self, line_index, Rule.REPETITION,
                "resulting formula doesn't match dependency")


class InvalidRuleApplicationException(Exception):
    def __init__(self, deduction, line_index, rule, msg=None):
        if msg is None:
            msg = 'No info'
        super().__init__(f'{rule.name}: {msg}')

        self.deduction = deduction
        self.line_index = line_index
        self.rule = rule
