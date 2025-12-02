from abc import ABC
import uuid

from create_entites.person.person import PersonCreateEntity
from entities.person.person import Person
from repositories.person.repository import PersonRepository
from services.balance_service import BalanceService


class PersonService(ABC):
    def __init__(self) -> None:
        self.balance_service = BalanceService()

        self.person_repository: PersonRepository

    def get_person(self, person_id: uuid.UUID) -> Person:
        return self.person_repository.get_person(person_id)

    def add_person(self, person_create_entity: PersonCreateEntity) -> Person:
        return self.person_repository.add_person(person_create_entity)

    def check_password(self, password_hash: str) -> bool:
        return self.password_hash == password_hash

    def get_balance(self) -> float:
        return self.balance
