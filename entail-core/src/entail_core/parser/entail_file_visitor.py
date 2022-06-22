from abc import ABC

from entail_core.entail_file import EntailFile
from entail_core.substitution import Substitution, DuplicatePredVarException
from entail_core.theorem_import import TheoremImport
from .ast_processing_exceptions import \
    DuplicatePredVarInSubstitutionException
from .deduction_visitor import DeductionVisitor


class EntailFileVisitor(DeductionVisitor, ABC):
    """Handles the whole AST"""

    def __init__(self, pred_vars=None):
        super().__init__(pred_vars=pred_vars)

    def visitStart(self, ctx):
        imports = [self.visit(import_ctx) for import_ctx in ctx.theoremImports]
        substitutions = [self.visit(sub_ctx) for sub_ctx in ctx.substitutions]
        deduction = self.visit(ctx.deduction())
        return EntailFile(deduction, imports, substitutions)

    def visitTheoremImport(self, ctx):
        theorem = self.visit(ctx.theorem)
        path = ctx.filepath.text
        path_without_quotes = path[1:-1]
        return TheoremImport(theorem, path_without_quotes)

    def visitSubstitution(self, ctx):
        theorem = self.visit(ctx.theorem)
        result = self.visit(ctx.result)
        specs = [self.visit(spec_ctx) for spec_ctx in ctx.specs]
        try:
            return Substitution(theorem, result, specs)
        except DuplicatePredVarException as e:
            raise DuplicatePredVarInSubstitutionException(ctx, e)

    def visitSpec(self, ctx):
        substituted_formula = self.visit(ctx.substituted)
        substitute_formula = self.visit(ctx.substitute)
        return substituted_formula, substitute_formula
