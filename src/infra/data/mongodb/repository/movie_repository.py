from infra.data.mongodb.context.mongodb_context import DynamoDBContext

from domain.interfaces.repository_interface import (
    RepositoryInterface,
)
from infra.data.mongodb.mappings.model_to_domain_mapping import (
    MovieModelToDomain as DomainMapper,
)
from domain.models.movie import Movie
from dataclasses import dataclass
from typing import Any, List
import uuid


@dataclass(repr=False, eq=False)
class MovieRepository(RepositoryInterface):
    context: DynamoDBContext

    def __post_init__(self):
        self.__db_set = self.context.customers
        self.__keys = ("id", "Item", "Items", "add", "update")

    def add(self, movie: Movie) -> bool:
        response = self.__add_or_update(movie, self.__keys[3])
        return response is not None

    def update(self, movie: Movie) -> bool:
        response = self.__add_or_update(movie, self.__keys[4])
        return response is not None

    def remove(self, id: uuid.UUID) -> bool:
        response = self.__db_set.delete_item(Key={self.__keys[0]: str(id)})
        return response is not None

    def get_all(self) -> List[Movie]:
        response = self.__db_set.scan()
        if response and self.__keys[2] in response:
            return DomainMapper.to_domain_list(response[self.__keys[2]])
        return None

    def get_by_id(self, id: uuid.UUID) -> Movie:
        response = self.__db_set.get_item(Key={self.__keys[0]: str(id)})
        if response and self.__keys[1] in response:
            return DomainMapper.to_domain(response[self.__keys[1]])
        return None


    def __add_or_update(self, movie: Movie, action: str) -> Any:
        existing_movie = self.get_by_id(movie.id)
        if action == self.__keys[4] and not existing_movie:
            return None
        data = self.__build_data(movie, existing_movie)
        response = self.__db_set.put_item(Item=data)
        return response

    def __build_data(self, movie: Movie, existing_movie: Movie) -> dict:
        data = {
            "id": str(movie.id),
            "name": movie.name,
        }

        if existing_movie and movie.id != existing_movie.id:
            data["id"] = str(existing_movie.id)

        return data
