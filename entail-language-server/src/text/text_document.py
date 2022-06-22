class TextDocument:
    @staticmethod
    def _text_to_lines(text):
        # Add "X" because otherwise `splitlines` will leave out the last line
        # if it's empty.
        lines = (text + 'X').splitlines()

        # Remove the extra "X" from the last line.
        lines[-1] = lines[-1][:-1]

        return lines

    def __init__(self, text):
        self._lines = self._text_to_lines(text)

    def apply_changes(self, changes):
        for change in changes:
            self.apply_change(change)

    def apply_change(self, change):
        change_lines = self._text_to_lines(change.text)
        start_pos = change.range.start
        end_pos = change.range.end

        prefix_to_keep = self._lines[start_pos.line][:start_pos.char]
        change_lines[0] = prefix_to_keep + change_lines[0]

        suffix_to_keep = self._lines[end_pos.line][end_pos.char:]
        change_lines[-1] += suffix_to_keep

        self._lines[start_pos.line:end_pos.line + 1] = change_lines

    def get_text(self):
        return '\n'.join(self._lines)

    def __eq__(self, other):
        if not isinstance(other, TextDocument):
            return False
        else:
            return self._lines == other._lines

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.get_text()
