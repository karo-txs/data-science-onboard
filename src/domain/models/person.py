from domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Person(Entity):
    name: str
    url: str