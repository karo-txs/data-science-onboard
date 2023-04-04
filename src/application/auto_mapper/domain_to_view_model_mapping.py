from application.view_models.movie_view_model import MovieViewModel
from application.view_models.genre_view_model import GenreViewModel
from application.view_models.person_view_model import PersonViewModel
from application.view_models.rating_view_model import RatingViewModel
from domain.models.genre import Genre
from domain.models.person import Person
from domain.models.rating import Rating
from domain.models.movie import Movie
from typing import List


class MovieDomainToViewModel:

    @staticmethod
    def to_view_model(movie: Movie) -> MovieViewModel:
        if movie:
            return MovieViewModel(
                name=movie.name,
                id=movie.id,
                url=movie.url,
                description=movie.description,
                rating=RatingDomainToViewModel.to_view_model(movie.rating),
                contentRating=movie.contentRating,
                genr=GenreDomainToViewModel.to_view_models(movie.genre),
                datePublished=movie.datePublished,
                keywords=movie.keywords,
                duration=movie.duration,
                actor=PersonDomainToViewModel.to_view_models(movie.actor),
                director=PersonDomainToViewModel.to_view_models(movie.director),
                creator=PersonDomainToViewModel.to_view_models(movie.creator),
            )

    @staticmethod
    def to_view_models(movies: List[Movie]) -> List[MovieViewModel]:
        movie_vms = list()
        if movies:
            for customer in movies:
                movie_vms.append(MovieDomainToViewModel.to_view_model(customer))
        return movie_vms

class RatingDomainToViewModel:

    @staticmethod
    def to_view_model(rating: Rating) -> RatingViewModel:
        if rating:
            return RatingViewModel(
            )

class GenreDomainToViewModel:

    @staticmethod
    def to_view_model(genre: Genre) -> GenreViewModel:
        if genre:
            return GenreViewModel(
                id=genre.id,
                name=genre.name
            )
    
    @staticmethod
    def to_view_models(genres: List[Genre]) -> List[GenreViewModel]:
        genre_vms = list()
        if genres:
            for g in genres:
                genre_vms.append(GenreDomainToViewModel.to_view_model(g))
        return genre_vms

class PersonDomainToViewModel:

    @staticmethod
    def to_view_model(person: Person) -> PersonViewModel:
        if person:
            return PersonViewModel(
                id=person.id,
                name=person.name,
                url=person.url
            )
    
    @staticmethod
    def to_view_models(persons: List[Person]) -> List[PersonViewModel]:
        person_vms = list()
        if persons:
            for p in persons:
                person_vms.append(PersonDomainToViewModel.to_view_model(p))
        return person_vms
