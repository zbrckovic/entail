"""Translation between model and types from pygls library."""

from entail_core.text import Range, Position
from entail_core.text_document_exception import TextDocumentException
from pygls import lsp
from pygls.lsp import Diagnostic, DiagnosticSeverity, \
    DiagnosticRelatedInformation, Location

from language_description.describe_position import Description
from text.change import Change

source = 'entail'


def to_hover(description: Description) -> lsp.Hover:
    return lsp.Hover(
        contents=description.description,
        range=from_range(description.range)
    )


def to_change(change: lsp.TextDocumentContentChangeEvent) -> Change:
    change_range = None
    if change.range is not None:
        change_range = to_range(change.range)
    return Change(change.text, change_range)


def to_range(text_range: lsp.Range) -> Range:
    start_pos = to_position(text_range.start)
    end_pos = to_position(text_range.end)
    return Range(start_pos, end_pos)


def from_range(text_range: Range) -> lsp.Range:
    start_pos = from_position(text_range.start)
    end_pos = from_position(text_range.end)
    return lsp.Range(start=start_pos, end=end_pos)


def to_position(pos: lsp.Position) -> Position:
    return Position(pos.line, pos.character)


def from_position(pos: Position) -> lsp.Position:
    return lsp.Position(line=pos.line, character=pos.char)


def error_to_diagnostic(error: TextDocumentException, uri):
    if len(error.related_info) > 0:
        related_information = [
            related_info_item_to_diagnostic_related_info(uri, item)
            for item in error.related_info]
    else:
        related_information = None

    return Diagnostic(
        range=from_range(error.range),
        message=error.message,
        source=source,
        severity=DiagnosticSeverity.Error,
        related_information=related_information
    )


def related_info_item_to_diagnostic_related_info(uri, item):
    location = Location(uri=uri, range=from_range(item.range))
    return DiagnosticRelatedInformation(location=location,
                                        message=item.message)
