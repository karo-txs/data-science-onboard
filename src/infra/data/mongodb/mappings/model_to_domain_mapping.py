from domain.models.movie import Movie
from typing import List
import uuid


class MovieModelToDomain:
    @staticmethod
    def to_domain(item: dict) -> Movie:
        return Movie(
            uuid.UUID(item["id"]),
            item["name"],
        )

    @staticmethod
    def to_domain_list(items: List[dict]) -> List[Movie]:
        return [MovieModelToDomain.to_domain(item) for item in items]
