from src.infra.data.pgsql.models.person_model import PersonModel
from src.infra.data.pgsql.models.movie_model import MovieModel
from infra.data.pgsql.models.base_model import BaseModel
from peewee import *


class MovieToCreatorModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    creator_id = ForeignKeyField(PersonModel, field="id")

    class Meta:
        table_name = "movies_to_creator"
