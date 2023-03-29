from dataclasses import dataclass, field
import uuid


@dataclass
class MovieViewModel:
    name: str = field(repr=False)
    id: uuid.UUID = field(default=None)
