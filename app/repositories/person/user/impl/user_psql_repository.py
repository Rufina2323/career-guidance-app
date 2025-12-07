from create_entites.person_db.impl.user import UserDBCreateEntity
from entities.balance import Balance
from entities.person.impl.user import User
from models.balance import Balance as BalanceModel
from models.deposit_transaction import DepositTransaction as DepositTransactionModel  # noqa: F401
from models.ml_request_transaction import (
    MLRequestTransaction as MLRequestTransactionModel,  # noqa: F401
)
from models.user import User as UserModel

from sqlmodel import Session
from database.engine import engine
from repositories.person.impl.person_psql_repository import PersonPSQLRepository
from repositories.person.user.user_repository import UserRepository


class UserPSQLRepository(UserRepository, PersonPSQLRepository):
    def add_person(self, user_db_create_entity: UserDBCreateEntity) -> User:
        balance_model = BalanceModel(
            amount=0,
        )

        user_model = UserModel(
            username=user_db_create_entity.username,
            email=user_db_create_entity.email,
            password_hash=user_db_create_entity.password_hash,
            balance=balance_model,
        )

        with Session(engine) as session:
            session.add(balance_model)
            session.add(user_model)
            session.commit()

            user = User(
                user_id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                balance=Balance(
                    amount=balance_model.amount,
                ),
            )

        return user
