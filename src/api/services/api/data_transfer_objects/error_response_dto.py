from dataclasses import dataclass, field
from typing import List


@dataclass(eq=False)
class ErrorResponseDto:
    state: str
    errors: List[str] = field(default_factory=list())
