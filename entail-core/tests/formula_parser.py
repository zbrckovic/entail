from antlr4 import CommonTokenStream, BailErrorStrategy, InputStream
from antlr4.error.ErrorListener import ErrorListener

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.antlr.EntailParser import EntailParser
from entail_core.parser.formula_visitor import FormulaVisitor


class _EntailErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        raise ValueError(msg)


class FormulaParser:
    def __init__(self):
        self.pred_vars = {}

    def parse(self, text):
        in_stream = InputStream(text)
        lexer = EntailLexer(in_stream)
        token_stream = CommonTokenStream(lexer)
        parser = EntailParser(token_stream)

        parser._errHandler = BailErrorStrategy()
        parser.addErrorListener(_EntailErrorListener())

        tree = parser.rootFormula()
        return FormulaVisitor(self.pred_vars).visit(tree)
