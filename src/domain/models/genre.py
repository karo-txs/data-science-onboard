from domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Genre:
    name: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
        }
