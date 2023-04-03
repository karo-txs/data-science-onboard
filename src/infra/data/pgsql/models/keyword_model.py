from infra.data.pgsql.models.base_model import BaseModel
from peewee import *


class KeywordModel(BaseModel):
    value = TextField(primary_key=True, unique=True)

    class Meta:
        table_name = "keywords"