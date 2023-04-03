from domain.models.movie import Movie
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import uuid

@dataclass(init=False, repr=False, eq=False)
class RepositoryInterface(ABC):

    @abstractmethod
    def add(self, obj: any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[any]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: uuid.UUID) -> any:
        raise NotImplementedError
