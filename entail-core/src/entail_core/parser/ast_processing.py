from entail_core.model.deduction.rule import rule_arities
from entail_core.text.text_document_exception import TextDocumentException, \
    RelatedErrorInfo
from .ast_processing_exceptions import UnexpectedLineNumberException, \
    DependencyLineNumberOutOfRangeException, DuplicateDependencyException, \
    InvalidDependencyPremisesException, PremiseEliminationException, \
    RuleArityException, DuplicatePredVarInSubstitutionException
from .entail_file_visitor import EntailFileVisitor
from .formula_visitor import AmbiguousPredVarVisitedException
from .util import get_token_range, get_tree_range


def process_ast(tree):
    visitor = EntailLanguageServerVisitor()
    return visitor.visit(tree)


class EntailLanguageServerVisitor(EntailFileVisitor):
    """Visits AST nodes, stores some summary information in its own fields and
    produces the model.

    Visitor expects a valid AST without syntax errors. If there were syntax
    errors and visitor is called on such AST, it might yield unexpected
    results."""

    def __init__(self, pred_vars=None):
        super().__init__(pred_vars=pred_vars)

        self.pred_var_occurrences = {}
        """Collects all non-conflicting occurrences of predicate variables."""

    def _register_pred_var_occurrence(self, ctx, pred_var):
        occurrences = self.pred_var_occurrences.get(pred_var)
        if occurrences is None:
            occurrences = []
            self.pred_var_occurrences[pred_var] = occurrences
        occurrences.append(ctx)

    def visitDeduction(self, ctx):
        try:
            return super().visitDeduction(ctx)
        except UnexpectedLineNumberException as e:
            msg = f'Line number should be {e.expected_line_number}.'
            range_ = get_token_range(e.ctx.lineNumber)
            raise TextDocumentException(msg, range_)
        except DependencyLineNumberOutOfRangeException as e:
            msg = f'Line number {e.line_number} out of range.'
            range_ = get_token_range(e.token)
            raise TextDocumentException(msg, range_)
        except InvalidDependencyPremisesException as e:
            msg = f'Dependency {e.dependency_line_number} depends on ' \
                  f'premises {e.offending_premises} which are not in force ' \
                  f'at line {e.line_number}.'
            range_ = get_tree_range(e.ctx)
            raise TextDocumentException(msg, range_)
        except PremiseEliminationException as e:
            msg = 'There is no premise to eliminate.'
            range_ = get_tree_range(e.ctx)
            raise TextDocumentException(msg, range_)
        except DuplicateDependencyException as e:
            msg = f'Duplicate dependency {e.line_number}.'
            range_ = get_token_range(e.token2)
            related_info = RelatedErrorInfo(
                get_token_range(e.token1),
                'Duplicate')
            raise TextDocumentException(msg, range_, [related_info])
        except RuleArityException as e:
            msg = f'Invalid number of dependencies - rule {e.rule.name} ' \
                  f'requires {rule_arities[e.rule]} dependencies but got ' \
                  f'{e.arity}.'
            range_ = get_tree_range(e.ctx)
            raise TextDocumentException(msg, range_)

    def visitAtomicFormula(self, ctx):
        try:
            formula = super().visitAtomicFormula(ctx)
            self._register_pred_var_occurrence(ctx, formula.pred_var)
            return formula
        except AmbiguousPredVarVisitedException as e:
            related_occurrences = self.pred_var_occurrences[
                e.existing_pred_var]

            related_info = []
            for related_occurrence in related_occurrences:
                msg = 'Conflicting occurrence'
                related_info_item = RelatedErrorInfo(
                    get_token_range(related_occurrence.predVar),
                    msg)
                related_info.append(related_info_item)

            text_range = get_token_range(ctx.predVar)
            msg = 'Predicate variable was reused with different meaning.'
            raise TextDocumentException(msg, text_range, related_info)

    def visitSubstitution(self, ctx):
        try:
            return super().visitSubstitution(ctx)
        except DuplicatePredVarInSubstitutionException as e:
            msg = f'Predicate {e.cause.pred_var} variable occurs ' \
                  f'multiple times in the substitution.'

            [first_index, *rest_indexes] = e.cause.indexes
            range_ = get_tree_range(e.ctx.specs[first_index])
            related_infos = [
                RelatedErrorInfo(get_tree_range(e.ctx.specs[i]), 'Duplicate')
                for i in rest_indexes]
            raise TextDocumentException(msg, range_, related_infos)
