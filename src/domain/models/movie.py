from domain.models.entity import Entity
from dataclasses import dataclass

@dataclass
class Movie(Entity):
    name: str
