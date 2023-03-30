from src.domain.models.person import Person
from src.domain.core.entity import Entity
from domain.models.rating import Rating
from domain.models.genre import Genre
from dataclasses import dataclass
from typing import List

@dataclass
class Movie(Entity):
    type: str
    name: str
    url: str
    description: str
    rating: Rating
    contentRating: str
    genre: List[Genre]
    datePublished: str
    keywords: List[str]
    duration: str
    actor: List[Person]
    director: List[Person]
    creator: List[Person]
