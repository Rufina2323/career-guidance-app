from create_entites.person_db.impl.admin import AdminDBCreateEntity
from entities.balance import Balance
from entities.person.impl.admin import Admin
from entities.person.impl.user import User

import uuid
from sqlalchemy.exc import NoResultFound

from models.balance import Balance as BalanceModel
from models.deposit_transaction import DepositTransaction as DepositTransactionModel  # noqa: F401
from models.ml_request_transaction import (
    MLRequestTransaction as MLRequestTransactionModel,  # noqa: F401
)
from models.person import Role, Person as PersonModel

from sqlmodel import Session, select
from database.engine import engine
from repositories.person.admin.admin_repository import AdminRepository
from repositories.person.impl.person_psql_repository import PersonPSQLRepository


class AdminPSQLRepository(AdminRepository, PersonPSQLRepository):
    def __init__(self):
        self.session_maker = Session

    def get_person(self, person_id: uuid.UUID) -> Admin | None:
        statement = (
            select(PersonModel)
            .where(PersonModel.id == person_id)
            .where(PersonModel.role == Role.ADMIN)
        )
        with self.session_maker(engine) as session:
            try:
                psql_user = session.exec(statement).one()
                return Admin(
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

    def add_person(self, admin_db_create_entity: AdminDBCreateEntity) -> Admin:
        balance_model = BalanceModel(
            amount=0,
        )

        user_model = PersonModel(
            username=admin_db_create_entity.username,
            email=admin_db_create_entity.email,
            password_hash=admin_db_create_entity.password_hash,
            balance=balance_model,
            role=Role.ADMIN,
        )

        with self.session_maker(engine) as session:
            session.add(balance_model)
            session.add(user_model)
            session.commit()

            admin = Admin(
                user_id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                balance=Balance(
                    amount=balance_model.amount,
                ),
            )

        return admin
