from infra.data.mongodb.db_connection import DbConnection
from dataclasses import dataclass, field
from typing import Any



@dataclass(repr=False, eq=False)
class DynamoDBContext:
    db_connection: DbConnection
    movies: Any = field(init=False)

    def __post_init__(self):
        self.__tables = self.db_connection.tables

        
        #self.__set_tables()

    def __set_tables(self):
        self.movies = self.__mongodb.Table(self.__tables[0])
