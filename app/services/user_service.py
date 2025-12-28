from repositories.person.user.impl.user_psql_repository import UserPSQLRepository
from repositories.person.repository import PersonRepository
from services.person_service import PersonService


class UserService(PersonService):
    def __init__(self) -> None:
        super().__init__()

        self.person_repository: PersonRepository = UserPSQLRepository()
