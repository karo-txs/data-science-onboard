from application.view_models.movie_view_model import MovieViewModel
from domain.models.movie import Movie

class MovieViewModelToDomainMapping:

    @staticmethod
    def to_domain(
        customer_vm: MovieViewModel,
    ) -> Movie:
        return Movie(
            id=customer_vm.id,
            name=customer_vm.name,
        )