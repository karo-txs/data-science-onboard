from domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Rating(Entity):
    ratingCount: int
    bestRating: float
    worstRating: float
    ratingValue: float
