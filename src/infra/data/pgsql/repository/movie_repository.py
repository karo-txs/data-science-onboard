from infra.data.pgsql.mappings.model_to_domain_mapping import (
    MovieModelToDomain,
    RatingModelToDomain,
    GenreModelToDomain,
    PersonModelToDomain,
    KeywordModelToDomain,
)
from src.domain.interfaces.repository_interface import (
    RepositoryInterface,
)
from infra.data.pgsql.context.pgsql_context import PgsqlContext
from domain.models.movie import Movie
from src.domain.models.person import Person
from src.domain.models.rating import Rating
from src.domain.models.genre import Genre
from dataclasses import dataclass
from typing import List
import uuid


@dataclass(repr=False, eq=False)
class MovieRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.movies
        self.rating_repository = RatingRepository(self.context)
        self.genre_repository = GenreRepository(self.context)
        self.movie_to_genre = MovieToGenreRepository(self.context)
        self.keyword_repository = KeywordRepository(self.context)
        self.movie_to_keyword = MovieToKeywordRepository(self.context)

    def add(self, movie: Movie) -> bool:
        self.rating_repository.add(movie.rating)

        response = self.__db_set.create(
            id=movie.id,
            name=movie.name,
            type=movie.type,
            url=movie.url,
            description=movie.description,
            rating=self.rating_repository.get_by_id(movie.rating.id),
            contentRating=movie.contentRating,
            datePublished=movie.datePublished,
            duration=movie.duration,
        )
        movie = self.get_by_id(movie.id)

        for genre in movie.genre:
            self.genre_repository.add(genre)
            self.movie_to_genre.add(movie, genre)

        for keyword in movie.keywords:
            self.keyword_repository.add(keyword)
            self.movie_to_keyword.add(movie, keyword)

        return response is not None

    def get_all(self) -> List[Movie]:
        movie_models = self.__db_set.select()

        movies = []
        for movie in movie_models:
            self.get_by_id(movie.id)

        return movies

    def get_by_id(self, id: uuid.UUID) -> Movie:
        movie_model = self.__db_set.select().where(self.__db_set.id == id)
        rating_model = RatingRepository.get_by_id(movie_model.rating.id)
        genre_model = GenreRepository.get_by_movie_id(id)
        keyword_model = KeywordRepository.get_by_movie_id(id)
        actor_model = PersonRepository.get_actors_by_movie_id(id)
        director_model = PersonRepository.get_director_by_movie_id(id)
        creator_model = PersonRepository.get_creator_by_movie_id(id)

        if movie_model:
            return MovieModelToDomain.to_domain(
                movie_model,
                rating_model,
                genre_model,
                keyword_model,
                actor_model,
                director_model,
                creator_model,
            )
        return None

@dataclass(repr=False, eq=False)
class GenreRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.genres
        self.__db_set_aux = self.context.movie_to_genre

    def add(self, genre: Genre) -> bool:
        response = self.__db_set.create(
            name=genre.name,
        )
        return response is not None

    def get_all(self) -> List[Genre]:
        genre_models = self.__db_set.select()
        if genre_models:
            return GenreModelToDomain.to_domain_list(genre_models)
        return None

    def get_by_id(self, movie_id: uuid.UUID) -> Genre:
        genre_models = self.__db_set.select().where(self.__db_set.id == id)
        if genre_models:
            return GenreModelToDomain.to_domain_list(genre_models)
        return None

    def get_by_movie_id(self, movie_id: uuid.UUID) -> List[Genre]:
        genre_models_aux = self.__db_set_aux.select().where(
            self.__db_set_aux.movie_id == movie_id
        )
        genre_models = []
        for genre_model in genre_models_aux:
            genre_models.append(
                self.__db_set.select().where(
                    self.__db_set.name == genre_model.genre_name
                )
            )

        if genre_models:
            return GenreModelToDomain.to_domain_list(genre_models)
        return []


@dataclass(repr=False, eq=False)
class RatingRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.ratings

    def add(self, rating: Rating) -> bool:
        response = self.__db_set.create(
            id=rating.id,
            ratingCount=rating.ratingCount,
            bestRating=rating.bestRating,
            worstRating=rating.worstRating,
            ratingValue=rating.ratingValue,
        )
        return response is not None

    def get_all(self) -> List[Rating]:
        rating_models = self.__db_set.select()
        if rating_models:
            return RatingModelToDomain.to_domain_list(rating_models)
        return None

    def get_by_id(self, id: uuid.UUID) -> Rating:
        rating_model = self.__db_set.select().where(self.__db_set.id == id)
        if rating_model:
            return RatingModelToDomain.to_domain(rating_model)
        return None


@dataclass(repr=False, eq=False)
class PersonRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.persons
        self.__db_set_actor = self.context.movie_to_actor
        self.__db_set_director = self.context.movie_to_director
        self.__db_set_creator = self.context.movie_to_creator

    def add(self, person: Person) -> bool:
        response = self.__db_set.create(
            id=uuid.uuid4(),
            name=person.name,
            url=person.url,
        )
        return response is not None

    def get_all(self) -> List[Person]:
        person_models = self.__db_set.select()
        if person_models:
            return PersonModelToDomain.to_domain_list(person_models)
        return None

    def get_by_id(self, id: uuid.UUID) -> Person:
        person_model = self.__db_set.select().where(self.__db_set.id == id)
        if person_model:
            return PersonModelToDomain.to_domain(person_model)
        return None

    def get_actors_by_movie_id(self, movie_id: uuid.UUID) -> List[Person]:
        person_models_aux = self.__db_set_actor.select().where(
            self.__db_set_actor.movie_id == movie_id
        )

        person_models = []
        for genre_model in person_models_aux:
            person_models.append(
                self.__db_set.select().where(self.__db_set.id == genre_model.genre_name)
            )

        if person_models:
            return PersonModelToDomain.to_domain_list(person_models)
        return []

    def get_director_by_movie_id(self, movie_id: uuid.UUID) -> List[Person]:
        person_models_aux = self.__db_set_director.select().where(
            self.__db_set_director.movie_id == movie_id
        )

        person_models = []
        for genre_model in person_models_aux:
            person_models.append(
                self.__db_set.select().where(self.__db_set.id == genre_model.genre_name)
            )

        if person_models:
            return PersonModelToDomain.to_domain_list(person_models)
        return []

    def get_creator_by_movie_id(self, movie_id: uuid.UUID) -> List[Person]:
        person_models_aux = self.__db_set_creator.select().where(
            self.__db_set_creator.movie_id == movie_id
        )

        person_models = []
        for genre_model in person_models_aux:
            person_models.append(
                self.__db_set.select().where(self.__db_set.id == genre_model.genre_name)
            )

        if person_models:
            return PersonModelToDomain.to_domain_list(person_models)
        return []


@dataclass(repr=False, eq=False)
class KeywordRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.keywords
        self.__db_set_aux = self.context.movie_to_keyword

    def add(self, keyword: str) -> bool:
        response = self.__db_set.create(
            value=keyword,
        )
        return response is not None

    def get_all(self) -> List[str]:
        keyword_models = self.__db_set.select()
        if keyword_models:
            return KeywordModelToDomain.to_domain_list(keyword_models)
        return None

    def get_by_id(self, movie_id: uuid.UUID) -> str:
        return None

    def get_by_movie_id(self, movie_id: uuid.UUID) -> List[str]:
        keyword_models_aux = self.__db_set_aux.select().where(
            self.__db_set_aux.movie_id == movie_id
        )
        keyword_models = []
        for keyword_model in keyword_models_aux:
            keyword_models.append(
                self.__db_set.select().where(self.__db_set.value == keyword_model.value)
            )

        if keyword_models:
            return KeywordModelToDomain.to_domain_list(keyword_models)

        return []


@dataclass(repr=False, eq=False)
class MovieToGenreRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.movie_to_genre

    def add(self, obj: any) -> bool:
        pass

    def add(self, movie: Movie, genre: Genre) -> bool:
        response = self.__db_set.create(
            id=uuid.uuid4(), movie_id=movie.id, genre_name=genre.name
        )
        return response is not None

    def get_all(self) -> List[Genre]:
        return None

    def get_by_id(self, id: uuid.UUID) -> Genre:
        return None


@dataclass(repr=False, eq=False)
class MovieToKeywordRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.movie_to_keyword

    def add(self, obj: any) -> bool:
        pass

    def add(self, movie: Movie, keyword: str) -> bool:
        response = self.__db_set.create(
            id=uuid.uuid4(), movie_id=movie.id, keyword=keyword
        )
        return response is not None

    def get_all(self) -> List[Genre]:
        return None

    def get_by_id(self, id: uuid.UUID) -> Genre:
        return None
