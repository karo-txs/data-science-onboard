from dataclasses import dataclass, field
import uuid

@dataclass
class GenreViewModel:
    name: str
    id: uuid.UUID = field(default=None)