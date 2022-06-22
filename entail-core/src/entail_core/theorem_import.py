from dataclasses import dataclass

from .formula.formula import Formula


@dataclass
class TheoremImport:
    theorem: Formula
    path: str

    def validate(self):
        # TODO: Implement this
        pass
