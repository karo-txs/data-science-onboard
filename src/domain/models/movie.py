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

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "rating": self.rating.to_dict(),
            "contentRating": self.contentRating,
            "datePublished": self.datePublished,
            "genre": [g.to_dict() for g in self.genre],
            "keywords": self.keywords,
            "actor": [a.to_dict() for a in self.actor],
            "director": [d.to_dict() for d in self.director],
            "creator": [c.to_dict() for c in self.creator],
        }
