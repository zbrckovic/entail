from antlr4 import Token
from antlr4.error.ErrorListener import ErrorListener

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.text import Position, Range
from entail_core.text_document_exception import TextDocumentException


class EntailErrorListener(ErrorListener):
    """Listens for parsing errors, interprets them and stores them in a list.
    """

    def __init__(self):
        super().__init__()

        self.errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        if offending_symbol.type == Token.EOF:
            text_len = 0
        elif offending_symbol.type == EntailLexer.NEWLINE:
            text_len = 0
        else:
            text_len = offending_symbol.stop - offending_symbol.start + 1

        start = Position(line - 1, column)
        end = Position(start.line, start.char + text_len)
        text_range = Range(start, end)
        error = TextDocumentException(msg, text_range)
        self.errors.append(error)
