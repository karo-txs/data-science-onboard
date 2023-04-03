from dataclasses import dataclass, field
import uuid

@dataclass
class GenreViewModel:
    id: uuid.UUID = field(default=None)
    name: str