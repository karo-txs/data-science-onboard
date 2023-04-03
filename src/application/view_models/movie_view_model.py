from src.application.view_models.genre_view_model import GenreViewModel
from src.application.view_models.person_view_model import PersonViewModel
from src.application.view_models.rating_view_model import RatingViewModel
from dataclasses import dataclass, field
from typing import List
import uuid


@dataclass
class MovieViewModel:
    id: uuid.UUID = field(default=None)
    type: str
    name: str
    url: str
    description: str
    rating: RatingViewModel
    contentRating: str
    genre: List[GenreViewModel]
    datePublished: str
    keywords: List[str]
    duration: str
    actor: List[PersonViewModel]
    director: List[PersonViewModel]
    creator: List[PersonViewModel]
