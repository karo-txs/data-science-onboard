from src.infra.data.pgsql.models.rating_model import RatingModel
from infra.data.pgsql.models.base_model import BaseModel
from peewee import *



class MovieModel(BaseModel):
    id = UUIDField(unique=True)
    name = TextField()
    type = TextField()
    url = TextField()
    description = TextField()
    rating: ForeignKeyField(RatingModel, field="id")
    contentRating = TextField()
    datePublished = TextField()
    duration = TextField()

    class Meta:
        table_name = "movies"
