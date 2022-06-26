from enum import auto, Enum


class Rule(Enum):
    PREMISE = auto()
    THEOREM = auto()
    A_IN = auto()
    A_OUT = auto()
    E_IN = auto()
    E_OUT = auto()
    IF_IN = auto()
    IF_OUT = auto()
    IFF_IN = auto()
    IFF_OUT = auto()
    AND_IN = auto()
    AND_OUT = auto()
    OR_IN = auto()
    OR_OUT = auto()
    NOT_IN = auto()
    NOT_OUT = auto()
    EXPLOSION = auto()
    REPETITION = auto()


rule_arities = dict([
    (Rule.PREMISE, 0),
    (Rule.THEOREM, 0),
    (Rule.A_IN, 1),
    (Rule.A_OUT, 1),
    (Rule.E_IN, 1),
    (Rule.E_OUT, 1),
    (Rule.IF_IN, 0),
    (Rule.IF_OUT, 2),
    (Rule.IFF_IN, 2),
    (Rule.IFF_OUT, 1),
    (Rule.AND_IN, 2),
    (Rule.AND_OUT, 1),
    (Rule.OR_IN, 1),
    (Rule.OR_OUT, 3),
    (Rule.NOT_IN, 2),
    (Rule.NOT_OUT, 1),
    (Rule.EXPLOSION, 2),
    (Rule.REPETITION, 1),
])
