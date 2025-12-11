import datetime
from entities.balance import Balance

import uuid

from entities.transaction.impl.deposit_transaction import DepositTransaction
from models.deposit_transaction import DepositTransaction as DepositTransactionModel  # noqa: F401

from sqlmodel import Session, select
from database.engine import engine
from repositories.transaction.deposit_transaction.deposit_transaction_repository import (
    DepositTransactionRepository,
)
from repositories.transaction.impl.transaction_psql_repository import (
    TransactionPSQLRepository,
)


class DepositTransactionPSQLRepository(
    DepositTransactionRepository, TransactionPSQLRepository
):
    def create_transaction(self, balance_id: uuid.UUID, amount: float) -> None:
        deposit_transaction_model = DepositTransactionModel(
            amount=amount,
            timestamp=datetime.datetime.now(),
            balance_id=balance_id,
        )

        with Session(engine) as session:
            session.add(deposit_transaction_model)
            session.commit()

    def get_all_transactions(self, balance_id: uuid.UUID) -> list[DepositTransaction]:
        statement = select(DepositTransactionModel).where(
            DepositTransactionModel.balance_id == balance_id
        )
        with Session(engine) as session:
            psql_deposit_transactions = session.exec(statement).all()
            deposit_transactions = []
            for tx in psql_deposit_transactions:
                deposit_transactions.append(
                    DepositTransaction(
                        balance=Balance(
                            amount=tx.balance.amount,
                        ),
                        amount=tx.amount,
                        timestamp=tx.timestamp,
                    )
                )

        return deposit_transactions
