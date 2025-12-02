import uuid
from create_entites.person.person import PersonCreateEntity
from entities.balance import Balance
from entities.person.person import Person
from repositories.person.repository import PersonRepository
from sqlmodel import Session, select
from database.engine import engine
from models.user import User as UserModel


class PersonPSQLRepository(PersonRepository):
    def add_person(self, person_create_entity: PersonCreateEntity) -> Person:
        raise NotImplementedError

    def get_person(self, person_id: uuid.UUID) -> Person:
        statement = select(UserModel).where(UserModel.id == person_id)
        with Session(engine) as session:
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
