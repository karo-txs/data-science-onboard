from api.domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Person(Entity):
    name: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
        }
