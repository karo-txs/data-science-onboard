from infra.data.pgsql.mappings.model_to_domain_mapping import (
    MovieModelToDomain as DomainMapper,
)
from domain.interfaces.movie_repository_interface import (
    MovieRepositoryInterface,
)
from infra.data.pgsql.context.pgsql_context import PgsqlContext
from domain.models.movie import Movie
from dataclasses import dataclass
from typing import List
import uuid


@dataclass(repr=False, eq=False)
class MovieRepository(MovieRepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.movies

    def add(self, movie: Movie) -> bool:
        response = self.__db_set.create(
            id=movie.id,
            name=movie.name,
        )
        return response is not None

    def update(self, movie: Movie) -> bool:
        response = (
            self.__db_set.update(
                name=movie.name,
            )
            .where(self.__db_set.id == movie.id)
            .execute()
        )
        return response is not None

    def remove(self, id: uuid.UUID) -> bool:
        response = self.__db_set.delete().where(self.__db_set.id == id).execute()
        return response is not None

    def get_all(self) -> List[Movie]:
        movie_models = self.__db_set.select()
        if movie_models:
            return DomainMapper.to_domain_list(movie_models)
        return None

    def get_by_id(self, id: uuid.UUID) -> Movie:
        movie_model = self.__db_set.select().where(self.__db_set.id == id)
        if movie_model:
            return DomainMapper.to_domain(movie_model)
        return None
