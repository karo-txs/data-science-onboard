from dataclasses import dataclass, field
import uuid

@dataclass
class PersonViewModel:
    name: str
    url: str
    id: uuid.UUID = field(default=None)