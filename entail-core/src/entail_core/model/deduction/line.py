from dataclasses import dataclass, field
from typing import Optional

from entail_core.model.formula.formula import Formula
from .rule import Rule


@dataclass
class Line:
    number: int
    """The ordinal number of this line counting from 1."""

    formula: Formula
    """The formula introduced in this line."""

    rule: Rule
    """The rule used to introduce this line."""

    dependencies: list[int] = field(default_factory=list)
    """The lines which were used as immediate dependencies of the rule."""

    premises: list[int] = field(default_factory=set)
    """All premises which are currently in force.

    These are all premises which have been introduced in some previous line, 
    but haven't been disposed yet."""

    rule_specific_data: Optional[dict] = None
