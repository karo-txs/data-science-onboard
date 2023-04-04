from domain.models.person import Person
from domain.core.entity import Entity
from domain.models.rating import Rating
from domain.models.genre import Genre
from dataclasses import dataclass, field
from typing import List

@dataclass
class Movie(Entity):
    type: str
    name: str
    url: str
    description: str
    rating: Rating
    contentRating: str
    datePublished: str
    duration: str
    genre: List[Genre] = field(default=None)
    keywords: List[str] = field(default=None)
    actor: List[Person] = field(default=None)
    director: List[Person] = field(default=None)
    creator: List[Person] = field(default=None)
