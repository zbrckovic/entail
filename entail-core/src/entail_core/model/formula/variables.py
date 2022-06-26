from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Var(ABC):
    id_: str
    """The unique identifier of this variable inside one Entail language file.
    """

    def __str__(self):
        return self.id_


@dataclass(frozen=True)
class PredVar(Var):
    """Predicate variable"""

    arity: int = 0
    """The number of terms required to form an atomic formula with this 
    predicate variable.
    
    When `arity` is zero, the predicate variable is actually a "propositional
    variable" - it can stand on it's own to form an atomic formula.
    """


@dataclass(frozen=True)
class IndVar(Var):
    """Individual variable"""
    pass
