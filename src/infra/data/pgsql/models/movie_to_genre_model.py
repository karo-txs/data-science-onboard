from src.infra.data.pgsql.models.genre_model import GenreModel
from src.infra.data.pgsql.models.movie_model import MovieModel
from infra.data.pgsql.models.base_model import BaseModel
from peewee import *


class MovieToGenreModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    genre_name = ForeignKeyField(GenreModel, field="name")

    class Meta:
        table_name = "movies_to_genre"
