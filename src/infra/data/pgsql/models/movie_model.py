from infra.data.pgsql.models.base_model import BaseModel
from peewee import TextField, DateField, UUIDField


class MovieModel(BaseModel):
    id = UUIDField(unique=True)
    name = TextField()

    class Meta:
        table_name = "movies"
