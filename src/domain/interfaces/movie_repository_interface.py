from domain.models.movie import Movie
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import uuid

@dataclass(init=False, repr=False, eq=False)
class MovieRepositoryInterface(ABC):

    @abstractmethod
    def add(self, movie: Movie) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, movie: Movie) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove(self, id: uuid.UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Movie]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> Movie:
        raise NotImplementedError
