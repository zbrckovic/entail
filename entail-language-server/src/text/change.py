from dataclasses import dataclass
from typing import Optional

from entail_core.text import Range


@dataclass
class Change:
    text: str
    range: Optional[Range]
