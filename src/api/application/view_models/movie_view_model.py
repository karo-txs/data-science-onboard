from api.application.view_models.genre_view_model import GenreViewModel
from api.application.view_models.person_view_model import PersonViewModel
from api.application.view_models.rating_view_model import RatingViewModel
from dataclasses import dataclass, field
from typing import List
import uuid


@dataclass
class MovieViewModel:
    type: str
    name: str
    description: str
    rating: RatingViewModel
    genre: List[GenreViewModel]
    year: int
    duration: int
    actor: List[PersonViewModel]
    director: List[PersonViewModel]
    id: uuid.UUID = field(default=None)
