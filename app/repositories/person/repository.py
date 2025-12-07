from abc import ABC, abstractmethod
import uuid

from create_entites.person_db.person import PersonDBCreateEntity
from entities.person.person import Person


class PersonRepository(ABC):
    @abstractmethod
    def add_person(self, person_create_entity: PersonDBCreateEntity) -> Person:
        raise NotImplementedError

    @abstractmethod
    def get_person(self, person_id: uuid.UUID) -> Person | None:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str) -> Person | None:
        raise NotImplementedError
