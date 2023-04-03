from infra.data.pgsql.models.base_model import BaseModel
from peewee import *


class PersonModel(BaseModel):
    name = TextField(primary_key=True, unique=True)
    url = TextField()

    class Meta:
        table_name = "persons"