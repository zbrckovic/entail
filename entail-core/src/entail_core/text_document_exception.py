from dataclasses import dataclass

from .text import Range


@dataclass
class TextDocumentException(Exception):
    def __init__(self, message, text_range, related_info=None):
        super().__init__(message)

        if related_info is None:
            related_info = []

        self.message = message
        self.range = text_range
        self.related_info = related_info


@dataclass
class RelatedErrorInfo:
    range: Range
    message: str
