from typing import List
from dataclasses import dataclass
from playhouse.postgres_ext import PostgresqlExtDatabase
import infra.data.pgsql.models.base_model as bm
from infra.data.pgsql.models.movie_model import MovieModel
from infra.data.pgsql.db_connection import DbConnection


@dataclass(repr=False, eq=False)
class PgsqlContext:
    db_connection: DbConnection

    def __post_init__(self):
        self.__connect(self.db_connection)
        self.__create_tables([MovieModel])
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

    def __create_tables(self, models: List):
        bm.database_proxy.create_tables(models)

    def __init_tables(self):
        self.movies = MovieModel
