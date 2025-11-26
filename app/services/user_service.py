from entities.person.impl.user import User
from services.person_service import PersonService


class UserService(PersonService):
    def request_deposit(self, user: User, amount: float) -> None:
        pass
