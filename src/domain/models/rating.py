from domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Rating(Entity):
    rating: str
    votes: int
    metascore: float
    imdb_ratings: float

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "rating": self.rating,
            "votes": self.votes,
            "metascore": self.metascore,
            "imdb_ratings": self.imdb_ratings,
        }

