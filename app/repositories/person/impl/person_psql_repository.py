import uuid
from create_entites.person_db.person import PersonDBCreateEntity
from entities.balance import Balance
from entities.person.person import Person
from repositories.person.repository import PersonRepository
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from database.engine import engine
from models.person import Person as PersonModel, Role


class PersonPSQLRepository(PersonRepository):
    def __init__(self):
        self.session_maker = Session

    def add_person(self, person_db_create_entity: PersonDBCreateEntity) -> Person:
        raise NotImplementedError

    def get_by_username(self, username: str) -> Person | None:
        statement = select(PersonModel).where(PersonModel.username == username)
        with self.session_maker(engine) as session:
            try:
                psql_user = session.exec(statement).one()
                return Person(
                    user_id=psql_user.id,
                    username=psql_user.username,
                    email=psql_user.email,
                    password_hash=psql_user.password_hash,
                    balance=Balance(
                        amount=psql_user.balance.amount,
                    ),
                )
            except NoResultFound:
                return None

    def get_person(self, person_id: uuid.UUID) -> Person | None:
        raise NotImplementedError

    def get_user_balance_id(self, person_id: uuid.UUID) -> uuid.UUID | None:
        statement = select(PersonModel).where(PersonModel.id == person_id)
        with self.session_maker(engine) as session:
            try:
                psql_user = session.exec(statement).one()
                return psql_user.balance_id

            except NoResultFound:
                return None

    def get_person_role(self, person_id: uuid.UUID) -> str | None:
        statement = select(PersonModel).where(PersonModel.id == person_id)
        with self.session_maker(engine) as session:
            try:
                psql_user = session.exec(statement).one()
                return psql_user.role

            except NoResultFound:
                return None

    def get_user_id_by_username(self, username: str) -> uuid.UUID:
        statement = select(PersonModel).where(PersonModel.username == username)
        with self.session_maker(engine) as session:
            psql_user = session.exec(statement).first()
            return psql_user.id

    def get_all_users(self) -> list[Person]:
        statement = select(PersonModel)
        with self.session_maker(engine) as session:
            psql_users = session.exec(statement).all()
            users = []
            for psql_user in psql_users:
                users.append(PersonModel.to_domain(psql_user))
            return users
