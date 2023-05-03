from domain.interfaces.repository_interface import RepositoryInterface
from infra.data.pgsql.context.pgsql_context import PgsqlContext
from infra.data.pgsql.mappings.model_to_domain_mapping import *
from infra.data.pgsql.models.models import *
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
        self.person_repository = PersonRepository(self.context)

    def add(self, movie: Movie) -> bool:
        
        movie_db = self.get_by_name(movie.name)
        if movie_db:
            movie.id = movie_db.id
            print("Movie already exists.")
            return self.update(movie)

        response = self.__db_set.create(
            id=movie.id,
            name=movie.name,
            type=movie.type,
            description=movie.description,
            year=movie.year,
            duration=movie.duration,
        )
        self.rating_repository.add_aux(movie, movie.rating)

        for genre in movie.genre:
            self.genre_repository.add_aux(movie, genre)
        
        for actor in movie.actor:
            self.person_repository.add_aux(movie, actor, person_type=0)
        
        for director in movie.director:
            self.person_repository.add_aux(movie, director, person_type=1)

        return response is not None
    
    def update(self, movie: Movie):
        response = (
            self.__db_set.update(
                name=movie.name,
                type=movie.type,
                description=movie.description,
                year=movie.year,
                duration=movie.duration,
            )
            .where(self.__db_set.id == movie.id)
            .execute()
        )
        self.rating_repository.update(movie.rating)

        return response is not None


    def get_by_name(self, name: str) -> Movie:
        movie_model: MovieModel = self.__db_set.select().where(self.__db_set.name == name)
        if movie_model:
            return self.get_by_id(movie_model[0].id)
        else:
            return None

    def get_all(self) -> List[Movie]:
        movie_models: List[MovieModel] = self.__db_set.select()

        movies = []
        for movie in movie_models:
            movies.append(self.get_by_id(movie.id))

        return movies

    def get_by_id(self, id: uuid.UUID) -> Movie:
        movie_model: MovieModel = self.__db_set.select().where(self.__db_set.id == id)
        rating_model = self.rating_repository.get_by_movie_id(id)
        genre_model = self.genre_repository.get_by_movie_id(id)
        actor_model = self.person_repository.get_by_movie_id(id, person_type=0)
        director_model = self.person_repository.get_by_movie_id(id, person_type=1)

        if movie_model:
            return MovieModelToDomain.to_domain(
                movie_model,
                rating_model,
                genre_model,
                actor_model,
                director_model,
            )
        return None

@dataclass(repr=False, eq=False)
class GenreRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.genres
        self.__db_set_aux = self.context.movie_to_genre

    def add_aux(self, movie: Movie, genre: Genre) -> bool:
        self.add(genre)

        response = self.__db_set_aux.create(
            id=uuid.uuid4(), movie_id=movie.id, genre_name=genre.name
        )
        return response is not None

    def add(self, genre: Genre) -> bool:
        response = False
        try:
            response = self.__db_set.create(
                name=genre.name,
            )
        except:
            print("Genre already exists.")
        return response is not None

    def get_all(self) -> List[Genre]:
        genre_models = self.__db_set.select()
        if genre_models:
            return GenreModelToDomain.to_domain_list(genre_models)
        return None

    def get_by_id(self, id: uuid.UUID) -> Genre:
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
            genre = self.__db_set.select().where(self.__db_set.name == genre_model.genre_name)[0]
            genre_models.append(genre)
        if genre_models:
            return genre_models
       
        return []


@dataclass(repr=False, eq=False)
class RatingRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.ratings
        self.__db_set_aux = self.context.movie_to_rating
    
    def add_aux(self, movie: Movie, rating: Rating) -> bool:
        self.add(rating)

        response = self.__db_set_aux.create(
            id=uuid.uuid4(), movie_id=movie.id, rating_id=rating.id
        )
        return response is not None

    def add(self, rating: Rating) -> bool:
        response = self.__db_set.create(
            id=rating.id,
            rating=rating.rating,
            votes=rating.votes,
            metascore=rating.metascore,
            imdb_ratings=rating.imdb_ratings,
        )
        return response is not None

    def update(self, rating: Rating) -> bool:
        response = (
            self.__db_set.update( 
            rating=rating.rating,
            votes=rating.votes,
            metascore=rating.metascore,
            imdb_ratings=rating.imdb_ratings)
            .where(self.__db_set.id == rating.id)
            .execute()
        )
        return response is not None

    def get_all(self) -> List[Rating]:
        rating_models = self.__db_set.select()
        if rating_models:
            return RatingModelToDomain.to_domain_list(rating_models)
        return None

    def get_by_id(self, id: uuid.UUID) -> Rating:
        rating_models = self.__db_set.select().where(
            self.__db_set.id == id
        )

        if rating_models:
            return RatingModelToDomain.to_domain(rating_models)
        return None
    
    def get_by_movie_id(self, id: uuid.UUID) -> Rating:
        rating_model_aux = self.__db_set_aux.select().where(self.__db_set_aux.movie_id == id)

        if rating_model_aux:
            rating_model = self.__db_set.select().where(self.__db_set.id == rating_model_aux[0].rating_id)
            return RatingModelToDomain.to_domain(rating_model[0])
        return None


@dataclass(repr=False, eq=False)
class PersonRepository(RepositoryInterface):
    context: PgsqlContext

    def __post_init__(self):
        self.__db_set = self.context.persons
        self.__db_aux = (self.context.movie_to_actor, 
                         self.context.movie_to_director)
    
    def add_aux(self, movie: Movie, person: Person, person_type: int) -> bool:
        self.add(person)

        response = self.__db_aux[person_type].create(
            id=uuid.uuid4(),
            person_id=person.id,
            movie_id=movie.id,
        )
        return response is not None

    def add(self, person: Person) -> bool:
        response = self.__db_set.create(
            id=person.id,
            name=person.name,
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

    def get_by_movie_id(self, movie_id: uuid.UUID, person_type: int) -> List[Person]:
        person_models_aux = self.__db_aux[person_type].select().where(
            self.__db_aux[person_type].movie_id == movie_id
        )

        person_models = []
        for person_model in person_models_aux:
            person = self.__db_set.select().where(self.__db_set.id == person_model.person_id)
            person_models.append(person[0])

        if person_models:
            return PersonModelToDomain.to_domain_list(person_models)
        return []
