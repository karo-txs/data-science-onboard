from infra.data.pgsql.models.base_model import BaseModel
from peewee import *



class MovieModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    name = TextField()
    type = TextField(null=True)
    description = TextField(null=True)
    year = IntegerField(null=True)
    duration = IntegerField(null=True)

    class Meta:
        table_name = "movies"

class PersonModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    name = TextField()

    class Meta:
        table_name = "persons"

class RatingModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    rating = TextField(null=True)
    votes = IntegerField(null=True)
    metascore = FloatField(null=True)
    imdb_ratings = FloatField(null=True)

    class Meta:
        table_name = "ratings"

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

class MovieToRatingModel(BaseModel):
    id = UUIDField(primary_key=True, unique=True)
    movie_id = ForeignKeyField(MovieModel, field="id")
    rating_id = ForeignKeyField(RatingModel, field="id")

    class Meta:
        table_name = "movies_to_rating"

