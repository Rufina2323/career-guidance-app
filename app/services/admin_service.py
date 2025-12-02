from entities.person.impl.user import User
from entities.transaction.transaction import Transaction
from repositories.person.admin.impl.admin_psql_repository import AdminPSQLRepository
from repositories.person.repository import PersonRepository
from services.person_service import PersonService


class AdminService(PersonService):
    def __init__(self) -> None:
        super().__init__()

        self.person_repository: PersonRepository = AdminPSQLRepository()

    def deposit_to_user(self, user: User, amount: float) -> None:
        self.person_repository.deposit_to_user(user, amount)

    def view_users_transactions(
        self, users: list[User]
    ) -> dict[User, list[Transaction]]:
        pass
