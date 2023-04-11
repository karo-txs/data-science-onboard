from domain.core.entity import Entity
from dataclasses import dataclass

@dataclass
class Rating(Entity):
    ratingCount: int
    bestRating: float
    worstRating: float
    ratingValue: float

    def to_dict(self) -> dict:
        return {
            "ratingCount": self.ratingCount,
            "bestRating": self.bestRating,
            "worstRating": self.worstRating,
            "ratingValue": self.ratingValue,
        }

