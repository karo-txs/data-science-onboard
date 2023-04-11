from infra.data.pgsql.models.base_model import BaseModel
from peewee import *



class MovieModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    name = TextField()
    type = TextField(null=True)
    url = TextField(null=True)
    description = TextField(null=True)
    contentRating = TextField(null=True)
    datePublished = TextField(null=True)
    duration = TextField(null=True)

    class Meta:
        table_name = "movies"

class PersonModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    name = TextField()
    url = TextField(null=True)

    class Meta:
        table_name = "persons"

class RatingModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    ratingCount = IntegerField(null=True)
    bestRating = FloatField(null=True)
    worstRating = FloatField(null=True)
    ratingValue = FloatField(null=True)

    class Meta:
        table_name = "ratings"

class KeywordModel(BaseModel):
    value = TextField(primary_key=True, unique=True)

    class Meta:
        table_name = "keywords"

class GenreModel(BaseModel):
    name = TextField(primary_key=True, unique=True)

    class Meta:
        table_name = "genres"

class MovieToActorModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    person_id = ForeignKeyField(PersonModel, field="id")

    class Meta:
        table_name = "movies_to_actor"

class MovieToKeywordModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    keyword = ForeignKeyField(KeywordModel, field="value")

    class Meta:
        table_name = "movies_to_keyword"

class MovieToGenreModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    genre_name = ForeignKeyField(GenreModel, field="name")

    class Meta:
        table_name = "movies_to_genre"

class MovieToDirectorModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    person_id = ForeignKeyField(PersonModel, field="id")

    class Meta:
        table_name = "movies_to_director"

class MovieToCreatorModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    person_id = ForeignKeyField(PersonModel, field="id")

    class Meta:
        table_name = "movies_to_creator"

class MovieToRatingModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    rating_id = ForeignKeyField(RatingModel, field="id")

    class Meta:
        table_name = "movies_to_rating"

