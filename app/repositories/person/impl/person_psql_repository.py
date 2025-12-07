import uuid
from create_entites.person_db.person import PersonDBCreateEntity
from entities.balance import Balance
from entities.person.person import Person
from repositories.person.repository import PersonRepository
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from database.engine import engine
from models.user import User as UserModel


class PersonPSQLRepository(PersonRepository):
    def add_person(self, person_db_create_entity: PersonDBCreateEntity) -> Person:
        raise NotImplementedError
    
    def get_by_username(self, username: str) -> Person | None:
        statement = select(UserModel).where(UserModel.username == username)
        with Session(engine) as session:
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
        statement = select(UserModel).where(UserModel.id == person_id)
        with Session(engine) as session:
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
