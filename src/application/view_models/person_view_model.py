from dataclasses import dataclass, field
import uuid

@dataclass
class PersonViewModel:
    id: uuid.UUID = field(default=None)
    name: str
    url: str