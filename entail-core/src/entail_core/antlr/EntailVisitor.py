# Generated from Entail.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EntailParser import EntailParser
else:
    from EntailParser import EntailParser

# This class defines a complete generic visitor for a parse tree produced by EntailParser.

class EntailVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EntailParser#start.
    def visitStart(self, ctx:EntailParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#theoremImport.
    def visitTheoremImport(self, ctx:EntailParser.TheoremImportContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#substitution.
    def visitSubstitution(self, ctx:EntailParser.SubstitutionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#spec.
    def visitSpec(self, ctx:EntailParser.SpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#deduction.
    def visitDeduction(self, ctx:EntailParser.DeductionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#line.
    def visitLine(self, ctx:EntailParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#ruleOfInference.
    def visitRuleOfInference(self, ctx:EntailParser.RuleOfInferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#ruleDependencies.
    def visitRuleDependencies(self, ctx:EntailParser.RuleDependenciesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#rootFormula.
    def visitRootFormula(self, ctx:EntailParser.RootFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#formula.
    def visitFormula(self, ctx:EntailParser.FormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#compRootFormula.
    def visitCompRootFormula(self, ctx:EntailParser.CompRootFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#compFormula.
    def visitCompFormula(self, ctx:EntailParser.CompFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#compRootBinaryFormula.
    def visitCompRootBinaryFormula(self, ctx:EntailParser.CompRootBinaryFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#compBinaryFormula.
    def visitCompBinaryFormula(self, ctx:EntailParser.CompBinaryFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#compUnaryFormula.
    def visitCompUnaryFormula(self, ctx:EntailParser.CompUnaryFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#binaryOperator.
    def visitBinaryOperator(self, ctx:EntailParser.BinaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#quantFormula.
    def visitQuantFormula(self, ctx:EntailParser.QuantFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#uniFormula.
    def visitUniFormula(self, ctx:EntailParser.UniFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#exiFormula.
    def visitExiFormula(self, ctx:EntailParser.ExiFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#atomicFormula.
    def visitAtomicFormula(self, ctx:EntailParser.AtomicFormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EntailParser#terms.
    def visitTerms(self, ctx:EntailParser.TermsContext):
        return self.visitChildren(ctx)



del EntailParser