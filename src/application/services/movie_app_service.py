from application.auto_mapper.domain_to_view_model_mapping import (
    MovieDomainToViewModel as ViewModelMapper,
)
from domain.interfaces.repository_interface import (
    RepositoryInterface,
)
from application.view_models.movie_view_model import MovieViewModel
from infra.data.pandasdb.db_to_dataframe import DBToDataframe
from infra.scrapy.imdb_scrapy import IMDBScrapy
from dataclasses import dataclass, field
from infra.plot.plotter import Plotter
from typing import List
import uuid


@dataclass(repr=False, eq=False)
class MovieAppService:
    movie_repository: RepositoryInterface = field(repr=False)
    movie_scrapy: IMDBScrapy = field(default=IMDBScrapy())

    def store_movies(self) -> bool:
        results = self.movie_scrapy.search_all()

        response = True

        for idx, movie in enumerate(results):
            if movie:
                response = self.movie_repository.add(movie)
                print(f"Movie Registred: {idx}/{(len(results))}")
                if response == False:
                    break

        return response

    def graphs_generate(self) -> bool:
        movies = self.movie_repository.get_all()
        df = DBToDataframe.convert(movies)
        df.to_csv("results/test.cvs")

        plotter = Plotter(df)

        return True

    def get_all(self) -> List[MovieViewModel]:
        movies = self.movie_repository.get_all()
        movie_vms = ViewModelMapper.to_view_models(movies)
        return movie_vms

    def get_by_id(self, id: uuid.UUID) -> MovieViewModel:
        movies = self.movie_repository.get_by_id(id)
        movie_vm = ViewModelMapper.to_view_model(movies)
        return movie_vm
