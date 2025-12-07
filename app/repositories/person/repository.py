from abc import ABC, abstractmethod
import uuid

from create_entites.person.person import PersonCreateEntity
from entities.person.person import Person


class PersonRepository(ABC):
    @abstractmethod
    def add_person(self, person_create_entity: PersonCreateEntity) -> Person:
        raise NotImplementedError

    @abstractmethod
    def get_person(self, person_id: uuid.UUID) -> Person:
        raise NotImplementedError
