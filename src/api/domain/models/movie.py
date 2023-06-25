from api.domain.models.person import Person
from api.domain.core.entity import Entity
from api.domain.models.rating import Rating
from api.domain.models.genre import Genre
from dataclasses import dataclass, field
from typing import List

@dataclass
class Movie(Entity):
    type: str
    name: str
    description: str
    rating: Rating
    year: int
    duration: int
    genre: List[Genre] = field(default=None)
    actor: List[Person] = field(default=None)
    director: List[Person] = field(default=None)

    def to_dict(self) -> dict:
        
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "rating": self.rating.rating if self.rating.rating else None,
            "votes": self.rating.votes if self.rating.votes else None,
            "metascore": self.rating.metascore if self.rating.metascore else None,
            "imdb_ratings": self.rating.imdb_ratings if self.rating.imdb_ratings else None,
            "duration": self.duration,
            "year": self.year,
            "genre": ",".join([g.name for g in self.genre]),
            "actor": ",".join([a.name for a in self.actor]),
            "director": ",".join([d.name for d in self.director]),
        }
