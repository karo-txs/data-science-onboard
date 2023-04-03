from infra.data.pgsql.models.base_model import BaseModel
from peewee import UUIDField, IntegerField, FloatField


class RatingModel(BaseModel):
    id = UUIDField(unique=True)
    ratingCount = IntegerField()
    bestRating = FloatField()
    worstRating = FloatField()
    ratingValue = FloatField()

    class Meta:
        table_name = "ratings"