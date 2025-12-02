from create_entites.person.impl.admin import AdminCreateEntity
from entities.balance import Balance
from entities.person.impl.admin import Admin
from entities.person.impl.user import User

from models.balance import Balance as BalanceModel
from models.deposit_transaction import DepositTransaction as DepositTransactionModel  # noqa: F401
from models.ml_request_transaction import (
    MLRequestTransaction as MLRequestTransactionModel,  # noqa: F401
)
from models.user import Role, User as UserModel
import bcrypt

from sqlmodel import Session, select
from database.engine import engine
from repositories.person.admin.admin_repository import AdminRepository
from repositories.person.impl.person_psql_repository import PersonPSQLRepository


class AdminPSQLRepository(AdminRepository, PersonPSQLRepository):
    def deposit_to_user(self, user: User, amount: float) -> None:
        statement = select(UserModel).where(UserModel.id == user.user_id)
        with Session(engine) as session:
            psql_user = session.exec(statement).one()
            psql_user.balance.amount += amount
            session.commit()

    def add_person(self, admin_create_entity: AdminCreateEntity) -> Admin:
        password_hash = bcrypt.hashpw(
            admin_create_entity.password.encode(), bcrypt.gensalt()
        )

        balance_model = BalanceModel(
            amount=0,
        )

        user_model = UserModel(
            username=admin_create_entity.username,
            email=admin_create_entity.email,
            password_hash=password_hash,
            balance=balance_model,
            role=Role.ADMIN,
        )

        with Session(engine) as session:
            session.add(balance_model)
            session.add(user_model)
            session.commit()

            admin = Admin(
                user_id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=password_hash,
                balance=Balance(
                    amount=balance_model.amount,
                ),
            )

        return admin
