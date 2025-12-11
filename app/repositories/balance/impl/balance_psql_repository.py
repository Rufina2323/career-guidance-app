import uuid
from entities.balance import Balance
from repositories.balance.repository import BalanceRepository
from sqlmodel import Session, select
from database.engine import engine
from models.balance import Balance as BalanceModel
from sqlalchemy.exc import NoResultFound


class BalancePSQLRepository(BalanceRepository):
    def get_balance(self, balance_id: uuid.UUID) -> Balance | None:
        with Session(engine) as session:
            try:
                find_balance = select(BalanceModel).where(BalanceModel.id == balance_id)
                psql_balance = session.exec(find_balance).one()
                return Balance(amount=psql_balance.amount)

            except NoResultFound:
                return None

    def deposit(self, balance_id: uuid.UUID, amount: float) -> None:
        statement = select(BalanceModel).where(BalanceModel.id == balance_id)
        with Session(engine) as session:
            psql_balance = session.exec(statement).one()
            psql_balance.amount += amount
            session.commit()

    def withdraw(self, balance_id: uuid.UUID, amount: float) -> None:
        statement = select(BalanceModel).where(BalanceModel.id == balance_id)
        with Session(engine) as session:
            psql_balance = session.exec(statement).one()
            psql_balance.amount -= amount
            session.commit()
