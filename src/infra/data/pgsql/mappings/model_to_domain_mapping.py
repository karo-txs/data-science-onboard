from infra.data.pgsql.models.movie_model import MovieModel
from domain.models.movie import Movie
from typing import List

class MovieModelToDomain:

    @staticmethod
    def to_domain(movie_model: MovieModel) -> Movie:
        if movie_model:
            return Movie(
                movie_model[0].id,
                movie_model[0].name,
            )
        return None

    @staticmethod
    def to_domain_list(movie_models: List[MovieModel]) -> List[Movie]:
        movies = list()
        for movie in movie_models:
            movies.append(
                Movie(
                    movie.id, movie.name
                )
            )
        return movies
