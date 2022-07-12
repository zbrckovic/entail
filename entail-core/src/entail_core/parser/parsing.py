"""Wrapper for antlr-generated parser."""

from dataclasses import field, dataclass

from antlr4 import InputStream, CommonTokenStream

from entail_core.antlr.EntailLexer import EntailLexer
from entail_core.antlr.EntailParser import EntailParser
from entail_core.text.text_document_exception import TextDocumentException
from .entail_error_listener import EntailErrorListener
from .entail_error_strategy import EntailErrorStrategy


def parse(text: str) -> 'ParserResult':
    """Parses text and returns the result."""

    in_stream = InputStream(text)

    lexer = EntailLexer(in_stream)
    token_stream = CommonTokenStream(lexer)
    parser = EntailParser(token_stream)

    error_listener = EntailErrorListener()
    error_strategy = EntailErrorStrategy()

    # This is deliberate because ANTLR4 doesn't generate setter for this field
    # when python is the target language. Nevertheless, setting the value of
    # this field is documented as a proper use-case in examples with Java as
    # the target language.
    parser._errHandler = error_strategy

    parser.removeErrorListeners()

    parser.addErrorListener(error_listener)

    tree = parser.start()

    return ParserResult(tree, error_listener.errors)


@dataclass
class ParserResult:
    tree: EntailParser.StartContext
    errors: list[TextDocumentException] = field(default_factory=list)
