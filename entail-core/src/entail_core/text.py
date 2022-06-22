"""Utils for referring to positions and ranges inside text.

When I say "text", I just mean a string which is potentially multi-lined and
lines are of natural length.
"""

from dataclasses import dataclass


@dataclass
class Position:
    """A specific position inside a text."""

    line: int
    """The line ordinal number counting from zero."""

    char: int
    """The character ordinal number counting from zero."""

    def __lt__(self, other):
        if self.line < other.line:
            return True
        return self.line == other.line and self.char < other.char

    def __le__(self, other):
        if self.line < other.line:
            return True
        return self.line == other.line and self.char <= other.char

    def __gt__(self, other):
        if self.line > other.line:
            return True
        return self.line == other.line and self.char > other.char

    def __ge__(self, other):
        if self.line > other.line:
            return True
        return self.line == other.line and self.char >= other.char


@dataclass
class Range:
    """The range between two specific positions inside text."""

    start: Position
    end: Position

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError('range start comes after range end')

    def includes(self, position):
        return self.start <= position < self.end
