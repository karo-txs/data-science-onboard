from dataclasses import dataclass, field
import uuid


@dataclass
class RatingViewModel:
    ratingCount: int
    bestRating: float
    worstRating: float
    ratingValue: float
    id: uuid.UUID = field(default=None)