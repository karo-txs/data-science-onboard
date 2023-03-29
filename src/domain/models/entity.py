from dataclasses import dataclass
from abc import ABC
import uuid


@dataclass(init=False)
class Entity(ABC):
    """Represents an entity object.

    Args:
        ABC (ABC): The abstract base class.

    Attributes:
        id (uuid.UUID): The entity Id.
    """

    id: uuid.UUID

    def __eq__(self, obj):
        if isinstance(obj, Entity):
            return self.id == obj.id
        return False
