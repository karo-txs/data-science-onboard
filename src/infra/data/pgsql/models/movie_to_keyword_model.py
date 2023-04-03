from src.infra.data.pgsql.models.keyword_model import KeywordModel
from src.infra.data.pgsql.models.movie_model import MovieModel
from infra.data.pgsql.models.base_model import BaseModel
from peewee import *


class MovieToKeywordModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie = ForeignKeyField(MovieModel, field="id")
    keyword = ForeignKeyField(KeywordModel, field="value")

    class Meta:
        table_name = "movies_to_keyword"
