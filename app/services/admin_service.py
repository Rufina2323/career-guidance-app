from entities.person.impl.user import User
from entities.transaction.transaction import Transaction
from services.person_service import PersonService


class AdminService(PersonService):
    def deposit_to_user(user: User, amount: float) -> None:
        pass

    def view_users_transactions(users: list[User]) -> dict[User, list[Transaction]]:
        pass
