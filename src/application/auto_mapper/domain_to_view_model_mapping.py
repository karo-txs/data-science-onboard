from application.view_models.movie_view_model import MovieViewModel
from domain.models.movie import Movie
from typing import List


class MovieDomainToViewModel:

    @staticmethod
    def to_view_model(movie: Movie) -> MovieViewModel:
        if movie:
            return MovieViewModel(
                name=movie.name,
                id=movie.id,
            )

    @staticmethod
    def to_view_models(movies: List[Movie]) -> List[MovieViewModel]:
        movie_vms = list()
        if movies:
            for customer in movies:
                movie_vms.append(MovieDomainToViewModel.to_view_model(customer))
        return movie_vms
