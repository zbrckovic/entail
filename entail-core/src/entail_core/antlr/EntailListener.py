# Generated from Entail.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EntailParser import EntailParser
else:
    from EntailParser import EntailParser

# This class defines a complete listener for a parse tree produced by EntailParser.
class EntailListener(ParseTreeListener):

    # Enter a parse tree produced by EntailParser#start.
    def enterStart(self, ctx:EntailParser.StartContext):
        pass

    # Exit a parse tree produced by EntailParser#start.
    def exitStart(self, ctx:EntailParser.StartContext):
        pass


    # Enter a parse tree produced by EntailParser#theoremImport.
    def enterTheoremImport(self, ctx:EntailParser.TheoremImportContext):
        pass

    # Exit a parse tree produced by EntailParser#theoremImport.
    def exitTheoremImport(self, ctx:EntailParser.TheoremImportContext):
        pass


    # Enter a parse tree produced by EntailParser#substitution.
    def enterSubstitution(self, ctx:EntailParser.SubstitutionContext):
        pass

    # Exit a parse tree produced by EntailParser#substitution.
    def exitSubstitution(self, ctx:EntailParser.SubstitutionContext):
        pass


    # Enter a parse tree produced by EntailParser#spec.
    def enterSpec(self, ctx:EntailParser.SpecContext):
        pass

    # Exit a parse tree produced by EntailParser#spec.
    def exitSpec(self, ctx:EntailParser.SpecContext):
        pass


    # Enter a parse tree produced by EntailParser#deduction.
    def enterDeduction(self, ctx:EntailParser.DeductionContext):
        pass

    # Exit a parse tree produced by EntailParser#deduction.
    def exitDeduction(self, ctx:EntailParser.DeductionContext):
        pass


    # Enter a parse tree produced by EntailParser#line.
    def enterLine(self, ctx:EntailParser.LineContext):
        pass

    # Exit a parse tree produced by EntailParser#line.
    def exitLine(self, ctx:EntailParser.LineContext):
        pass


    # Enter a parse tree produced by EntailParser#ruleOfInference.
    def enterRuleOfInference(self, ctx:EntailParser.RuleOfInferenceContext):
        pass

    # Exit a parse tree produced by EntailParser#ruleOfInference.
    def exitRuleOfInference(self, ctx:EntailParser.RuleOfInferenceContext):
        pass


    # Enter a parse tree produced by EntailParser#ruleDependencies.
    def enterRuleDependencies(self, ctx:EntailParser.RuleDependenciesContext):
        pass

    # Exit a parse tree produced by EntailParser#ruleDependencies.
    def exitRuleDependencies(self, ctx:EntailParser.RuleDependenciesContext):
        pass


    # Enter a parse tree produced by EntailParser#rootFormula.
    def enterRootFormula(self, ctx:EntailParser.RootFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#rootFormula.
    def exitRootFormula(self, ctx:EntailParser.RootFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#formula.
    def enterFormula(self, ctx:EntailParser.FormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#formula.
    def exitFormula(self, ctx:EntailParser.FormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#compRootFormula.
    def enterCompRootFormula(self, ctx:EntailParser.CompRootFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#compRootFormula.
    def exitCompRootFormula(self, ctx:EntailParser.CompRootFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#compFormula.
    def enterCompFormula(self, ctx:EntailParser.CompFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#compFormula.
    def exitCompFormula(self, ctx:EntailParser.CompFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#compRootBinaryFormula.
    def enterCompRootBinaryFormula(self, ctx:EntailParser.CompRootBinaryFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#compRootBinaryFormula.
    def exitCompRootBinaryFormula(self, ctx:EntailParser.CompRootBinaryFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#compBinaryFormula.
    def enterCompBinaryFormula(self, ctx:EntailParser.CompBinaryFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#compBinaryFormula.
    def exitCompBinaryFormula(self, ctx:EntailParser.CompBinaryFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#compUnaryFormula.
    def enterCompUnaryFormula(self, ctx:EntailParser.CompUnaryFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#compUnaryFormula.
    def exitCompUnaryFormula(self, ctx:EntailParser.CompUnaryFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#binaryOperator.
    def enterBinaryOperator(self, ctx:EntailParser.BinaryOperatorContext):
        pass

    # Exit a parse tree produced by EntailParser#binaryOperator.
    def exitBinaryOperator(self, ctx:EntailParser.BinaryOperatorContext):
        pass


    # Enter a parse tree produced by EntailParser#quantFormula.
    def enterQuantFormula(self, ctx:EntailParser.QuantFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#quantFormula.
    def exitQuantFormula(self, ctx:EntailParser.QuantFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#uniFormula.
    def enterUniFormula(self, ctx:EntailParser.UniFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#uniFormula.
    def exitUniFormula(self, ctx:EntailParser.UniFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#exiFormula.
    def enterExiFormula(self, ctx:EntailParser.ExiFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#exiFormula.
    def exitExiFormula(self, ctx:EntailParser.ExiFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#atomicFormula.
    def enterAtomicFormula(self, ctx:EntailParser.AtomicFormulaContext):
        pass

    # Exit a parse tree produced by EntailParser#atomicFormula.
    def exitAtomicFormula(self, ctx:EntailParser.AtomicFormulaContext):
        pass


    # Enter a parse tree produced by EntailParser#terms.
    def enterTerms(self, ctx:EntailParser.TermsContext):
        pass

    # Exit a parse tree produced by EntailParser#terms.
    def exitTerms(self, ctx:EntailParser.TermsContext):
        pass



del EntailParser