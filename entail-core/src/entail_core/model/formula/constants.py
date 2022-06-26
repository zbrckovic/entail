"""Logical constants"""

from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class TFOperator:
    """Truth-functional operator"""

    id_: str
    arity: int = 1

    def __str__(self):
        return self.id_


NEGATION = TFOperator('~')
CONJUNCTION = TFOperator('&', 2)
DISJUNCTION = TFOperator('|', 2)
CONDITIONAL = TFOperator('->', 2)
BICONDITIONAL = TFOperator('<->', 2)


class Quantifier(Enum):
    UNIVERSAL = auto()
    EXISTENTIAL = auto()
