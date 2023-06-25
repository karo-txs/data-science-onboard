from typing import List
from dataclasses import dataclass
from playhouse.postgres_ext import PostgresqlExtDatabase
import api.infra.data.pgsql.models.base_model as bm
from api.infra.data.pgsql.db_connection import DbConnection
from api.infra.data.pgsql.models.models import *


@dataclass(repr=False, eq=False)
class PgsqlContext:
    db_connection: DbConnection

    def __post_init__(self):
        self.__connect(self.db_connection)
        self.__create_tables()
        self.__init_tables()

    def __connect(self, db_connection: DbConnection):
        database = PostgresqlExtDatabase(
            db_connection.dbname,
            user=db_connection.user,
            password=db_connection.password,
            host=db_connection.host,
            port=db_connection.port,
        )
        bm.database_proxy.initialize(database)

    def __create_tables(self):
        models = [MovieModel,
                  RatingModel, 
                  GenreModel, 
                  PersonModel,
                  MovieToActorModel, 
                  MovieToDirectorModel,
                  MovieToGenreModel, 
                  MovieToRatingModel]
        
        for model in models:
            bm.database_proxy.create_tables([model])

    def __init_tables(self):
        self.ratings = RatingModel
        self.movies = MovieModel
        self.genres = GenreModel
        self.persons = PersonModel
        self.movie_to_actor = MovieToActorModel
        self.movie_to_director = MovieToDirectorModel
        self.movie_to_genre = MovieToGenreModel
        self.movie_to_rating = MovieToRatingModel
