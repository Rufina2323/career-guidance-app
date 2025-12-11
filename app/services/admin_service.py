import uuid
from repositories.person.admin.impl.admin_psql_repository import AdminPSQLRepository
from repositories.person.repository import PersonRepository
from services.person_service import PersonService


class AdminService(PersonService):
    def __init__(self) -> None:
        super().__init__()

        self.person_repository: PersonRepository = AdminPSQLRepository()

    def deposit_to_user(self, person_id: uuid.UUID, amount: float) -> None:
        balance_id = self.get_user_balance_id(person_id)
        if not balance_id:
            raise ValueError("User does not exist.")

        self.balance_service.deposit(balance_id, amount)
