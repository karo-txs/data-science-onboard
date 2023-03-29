from application.view_models.movie_view_model import MovieViewModel
from application.auto_mapper.view_model_to_domain_mapping import (
    MovieViewModelToDomainMapping as DomainMapper,
)
from application.auto_mapper.domain_to_view_model_mapping import (
    MovieDomainToViewModel as ViewModelMapper,
)
from services.api.auto_mapper.json_to_view_model_mapping import (
    GenericJsonToViewModelMapping as GenericViewModelMapper,
)
from domain.interfaces.movie_repository_interface import (
    MovieRepositoryInterface,
)
from dataclasses import dataclass, field
from domain.models.movie import Movie
from PyMovieDb import IMDB
from typing import List
import logging
import json
import uuid


@dataclass(repr=False, eq=False)
class MovieAppService:
    movie_repository: MovieRepositoryInterface = field(repr=False)

    def register(
        self, movie_vm: MovieViewModel
    ) -> bool:
        movie = DomainMapper.to_domain(movie_vm)
        logging.info(movie)
        return self.movie_repository.add(movie_vm)

    def store_movies(self) -> bool:
        imdb = IMDB()
        result = json.loads(imdb.search("love", year=2023))
        print(result["result_count"])

        response = True

        for movie in result["results"]:
            if movie:
                movie_vm = MovieViewModel(id=uuid.uuid4(), name=movie["name"])
                response = self.movie_repository.add(DomainMapper.to_domain(movie_vm))

                if(response == False):
                    break
        
        return response

    def update(
        self, movie_vm: MovieViewModel
    ) -> bool:
        movie = DomainMapper.to_domain(movie_vm)
        logging.info(movie)
        return self.movie_repository.update(movie)

    def remove(self, id: uuid.UUID) -> bool:
        return self.movie_repository.remove(id)

    def get_all(self) -> List[MovieViewModel]:
        movies = self.movie_repository.get_all()
        movie_vms = ViewModelMapper.to_view_models(movies)
        return movie_vms

    def get_by_id(self, id: uuid.UUID) -> MovieViewModel:
        movies = self.movie_repository.get_by_id(id)
        movie_vm = ViewModelMapper.to_view_model(movies)
        return movie_vm