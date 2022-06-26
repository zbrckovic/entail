from antlr4.Token import CommonToken

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.antlr.EntailParser import EntailParser
from entail_core.antlr.EntailVisitor import EntailVisitor
from entail_core.model.formula.constants import NEGATION, CONDITIONAL, CONJUNCTION, \
    DISJUNCTION, BICONDITIONAL, Quantifier
from entail_core.model.formula.formula import AtomicFormula, CompoundFormula, \
    QuantifiedFormula
from entail_core.model.formula.variables import PredVar, IndVar

PredVarOccurrencesMap = dict[PredVar, list[EntailParser.AtomicFormulaContext]]
PredVarOccurrenceMap = dict[PredVar, EntailParser.AtomicFormulaContext]


class FormulaVisitor(EntailVisitor):
    """Handles parts of AST which represent a formula.

    Builds a formula while visiting the AST nodes and returns it as a result of
    formula-visiting calls. It tracks visited predicate variables and raises an
    exception if ambiguity is detected.
    """

    def __init__(self, pred_vars=None):
        if pred_vars is None:
            pred_vars = {}

        self.pred_vars = pred_vars
        """Predicate variables mapped by their ids.
        
        Values are predicate variables visited during the processing of an
        AST and keys are their ids. This is useful to quickly lookup whether 
        a predicate variable with the same id has already been visited. If two 
        predicate variables have the same id, but are otherwise not equal, this 
        is considered an ambiguity and an exception is raised. Only the first
        among conflicting predicate variables will be stored inside this map.
        """

    def visitRootFormula(self, ctx):
        if ctx.compRootFormula() is not None:
            return self.visit(ctx.compRootFormula())
        if ctx.quantFormula() is not None:
            return self.visit(ctx.quantFormula())
        if ctx.atomicFormula() is not None:
            return self.visit(ctx.atomicFormula())

    def visitFormula(self, ctx):
        if ctx.compFormula() is not None:
            return self.visit(ctx.compFormula())
        if ctx.quantFormula() is not None:
            return self.visit(ctx.quantFormula())
        if ctx.atomicFormula() is not None:
            return self.visit(ctx.atomicFormula())

    def visitCompRootFormula(self, ctx):
        if ctx.compRootBinaryFormula() is not None:
            return self.visit(ctx.compRootBinaryFormula())
        if ctx.compUnaryFormula() is not None:
            return self.visit(ctx.compUnaryFormula())

    def visitCompFormula(self, ctx):
        if ctx.compBinaryFormula() is not None:
            return self.visit(ctx.compBinaryFormula())
        if ctx.compUnaryFormula() is not None:
            return self.visit(ctx.compUnaryFormula())

    def visitCompRootBinaryFormula(self, ctx):
        return self._visit_comp_binary_formula(ctx)

    def visitCompBinaryFormula(self, ctx):
        return self._visit_comp_binary_formula(ctx)

    def _visit_comp_binary_formula(self, ctx):
        operator = self.visit(ctx.binaryOperator())
        left_formula = self.visit(ctx.lFormula)
        right_formula = self.visit(ctx.rFormula)
        return CompoundFormula(operator, [left_formula, right_formula])

    def visitBinaryOperator(self, ctx):
        return self._resolve_binary_operator(ctx.operator)

    def visitCompUnaryFormula(self, ctx):
        operator = self._resolve_unary_operator(ctx.operator)
        formula = self.visit(ctx.formula())
        return CompoundFormula(operator, [formula])

    @staticmethod
    def _resolve_binary_operator(token: CommonToken):
        match token.type:
            case EntailLexer.CONJUNCTION:
                return CONJUNCTION
            case EntailLexer.DISJUNCTION:
                return DISJUNCTION
            case EntailLexer.CONDITIONAL:
                return CONDITIONAL
            case EntailLexer.BICONDITIONAL:
                return BICONDITIONAL
            case _:
                raise ValueError('unknown operator')

    @staticmethod
    def _resolve_unary_operator(token: CommonToken):
        match token.type:
            case EntailLexer.NEGATION:
                return NEGATION
            case _:
                raise ValueError('unknown operator')

    def visitQuantFormula(self, ctx: EntailParser.QuantFormulaContext):
        if ctx.uniFormula() is not None:
            return self.visit(ctx.uniFormula())
        if ctx.exiFormula() is not None:
            return self.visit(ctx.exiFormula())

    def visitUniFormula(self, ctx):
        ind_var = IndVar(ctx.indVar.text)
        formula = self.visit(ctx.formula())
        return QuantifiedFormula(Quantifier.UNIVERSAL, ind_var, formula)

    def visitExiFormula(self, ctx):
        ind_var = IndVar(ctx.indVar.text)
        formula = self.visit(ctx.formula())
        return QuantifiedFormula(Quantifier.EXISTENTIAL, ind_var, formula)

    def visitAtomicFormula(self, ctx):
        pred_var_id = ctx.predVar.text
        if ctx.terms() is not None:
            ind_vars = list(self.visit(ctx.terms()))
        else:
            ind_vars = []

        arity = len(ind_vars)
        pred_var = PredVar(pred_var_id, arity)

        self._validate_pred_var(ctx, pred_var)

        return AtomicFormula(pred_var, ind_vars)

    def visitTerms(self, ctx):
        for ind_var in ctx.indVars:
            yield IndVar(ind_var.text)

    def _validate_pred_var(self, ctx, pred_var):
        """Validates and stores the predicate variable."""

        existing_pred_var = self.pred_vars.get(pred_var.id_)

        if existing_pred_var is None:
            self.pred_vars[pred_var.id_] = pred_var
            return

        if pred_var != existing_pred_var:
            raise AmbiguousPredVarVisitedException(ctx,
                                                   existing_pred_var,
                                                   pred_var)


class AmbiguousPredVarVisitedException(Exception):
    def __init__(self, ctx, existing_pred_var, pred_var, msg=None):
        if msg is None:
            msg = 'found unequal predicate variables with the same id'
        self.ctx = ctx
        self.existing_pred_var = existing_pred_var
        self.pred_var = pred_var
        super().__init__(msg)
