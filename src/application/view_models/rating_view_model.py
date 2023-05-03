from dataclasses import dataclass, field
import uuid


@dataclass
class RatingViewModel:
    rating: str
    votes: int
    metascore: float
    imdb_ratings: float
    id: uuid.UUID = field(default=None)