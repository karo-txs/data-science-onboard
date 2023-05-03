from infra.data.pgsql.models.models import *
from domain.models.person import Person
from domain.models.rating import Rating
from domain.models.movie import Movie
from domain.models.genre import Genre
from typing import List


class MovieModelToDomain:
    @staticmethod
    def to_domain(
        movie_model: MovieModel,
        rating_model: RatingModel,
        genre_model: List[GenreModel],
        actor_models: List[PersonModel],
        director_models: List[PersonModel],
    ) -> Movie:
        if movie_model:
            return Movie(
                id=movie_model[0].id,
                name=movie_model[0].name,
                type=movie_model[0].type,
                description=movie_model[0].description,
                rating=RatingModelToDomain.to_domain(rating_model),
                genre=GenreModelToDomain.to_domain_list(genre_model),
                year=movie_model[0].year,
                duration=movie_model[0].duration,
                actor=PersonModelToDomain.to_domain_list(actor_models),
                director=PersonModelToDomain.to_domain_list(director_models),
            )
        return None

    @staticmethod
    def to_domain_list(movie_models: List[MovieModel]) -> List[Movie]:
        movies = list()
        for movie in movie_models:
            movies.append(MovieModelToDomain.to_domain(movie))
        return movies


class RatingModelToDomain:
    @staticmethod
    def to_domain(rating_model: RatingModel) -> Rating:
        if rating_model:
            return Rating(
                id=rating_model.id,
                rating=rating_model.rating,
                votes=rating_model.votes,
                metascore=rating_model.metascore,
                imdb_ratings=rating_model.imdb_ratings,
            )
        return None

    @staticmethod
    def to_domain_list(rating_models: List[RatingModel]) -> List[Rating]:
        ratings = list()
        for rating in rating_models:
            ratings.append(RatingModelToDomain.to_domain(rating))
        return ratings


class GenreModelToDomain:
    @staticmethod
    def to_domain(genre_model: GenreModel) -> Genre:
        if genre_model:
            return Genre(
                name=genre_model.name,
            )
        return None

    @staticmethod
    def to_domain_list(genre_models: List[GenreModel]) -> List[Genre]:
        genres = list()
        for genre in genre_models:
            if isinstance(genre, GenreModel):
                genres.append(GenreModelToDomain.to_domain(genre))
        return genres


class PersonModelToDomain:
    @staticmethod
    def to_domain(person_model: PersonModel) -> Person:
        if person_model:
            return Person(
                id=person_model.id,
                name=person_model.name,
            )
        return None

    @staticmethod
    def to_domain_list(person_models: List[PersonModel]) -> List[Person]:
        persons = list()
        for person in person_models:
            persons.append(PersonModelToDomain.to_domain(person))
        return persons
