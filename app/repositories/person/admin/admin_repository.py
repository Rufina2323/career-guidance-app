from entities.person.impl.user import User
from repositories.person.repository import PersonRepository
from abc import abstractmethod


class AdminRepository(PersonRepository):
    @abstractmethod
    def deposit_to_user(self, user: User, amount: float) -> None:
        raise NotImplementedError
