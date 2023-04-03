from dataclasses import dataclass, field
import uuid


@dataclass
class RatingViewModel:
    id: uuid.UUID = field(default=None)
    ratingCount: int
    bestRating: float
    worstRating: float
    ratingValue: float