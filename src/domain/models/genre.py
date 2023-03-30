from src.domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Genre(Entity):
    name: str