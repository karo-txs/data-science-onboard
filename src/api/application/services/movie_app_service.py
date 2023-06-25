from api.application.auto_mapper.domain_to_view_model_mapping import (
    MovieDomainToViewModel as ViewModelMapper,
)
from api.domain.interfaces.repository_interface import (
    RepositoryInterface,
)
from api.application.view_models.movie_view_model import MovieViewModel
from api.infra.data.pandasdb.db_to_dataframe import DBToDataframe
from ml.preprocessing.prepare_data import PrepareData
from api.infra.scrapy.imdb_scrapy import IMDBScrapy
from dataclasses import dataclass, field
from ml.functions.train import Train
from ml.functions.test import Test
from typing import List
import uuid


@dataclass(repr=False, eq=False)
class MovieAppService:
    movie_repository: RepositoryInterface = field(repr=False)
    movie_scrapy: IMDBScrapy = field(default=IMDBScrapy())
    X_train: any = field(default=None)
    X_test: any = field(default=None)
    y_train: any = field(default=None) 
    y_test: any = field(default=None)

    def update_database(self) -> bool:
        while self.movie_scrapy.have_movies:
            results = self.movie_scrapy.search_all()

            for idx, movie in enumerate(results):
                if movie:
                    response = self.movie_repository.add(movie)
                    print(f"Movie Registred: {idx}/{(len(results))}")

                    if response == False:
                        print(f"Error in register")

        return True

    def train(self) -> bool:
        movies = self.movie_repository.get_all()
        df = DBToDataframe.convert(movies)

        prepare_data = PrepareData(df, target="imdb_ratings", info_data={"name": "text", 
                                                                        "votes": "number",
                                                                        "duration": "number",
                                                                        "year": "number",
                                                                        "genre": "multi_label", 
                                                                        "actor": "multi_label",
                                                                        "director": "multi_label",})

        self.X_train, self.X_test, self.y_train, self.y_test = prepare_data.apply()
        train = Train(self.X_train, self.y_train, model_names=["svm", "lr", "et"]).run()

    def test(self) -> dict:
        test = Test(self.X_test, self.y_test, model_names=["svm", "lr", "et"]).run()
    
    def inference(self) -> dict:
        pass
