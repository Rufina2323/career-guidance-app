import uuid
from entities.transaction.transaction import Transaction
from repositories.transaction.deposit_transaction.deposit_transaction_repository import (
    DepositTransactionRepository,
)
from repositories.transaction.deposit_transaction.impl.deposit_transaction_psql_repository import (
    DepositTransactionPSQLRepository,
)
from repositories.transaction.ml_request_transaction.impl.ml_request_transaction_psql_repository import (
    MLRequestTransactionPSQLRepository,
)
from repositories.transaction.ml_request_transaction.ml_request_transaction_repository import (
    MLRequestTransactionRepository,
)


class TransactionService:
    def __init__(self) -> None:
        self.deposit_transaction_repository: DepositTransactionRepository = (
            DepositTransactionPSQLRepository()
        )
        self.ml_request_transaction_repository: MLRequestTransactionRepository = (
            MLRequestTransactionPSQLRepository()
        )

    def create_ml_request_transaction(
        self, ml_request_id: uuid.UUID, balance_id: uuid.UUID, amount: float
    ) -> None:
        self.ml_request_transaction_repository.create_transaction(
            ml_request_id, balance_id, amount
        )

    def create_deposit_transaction(self, balance_id: uuid.UUID, amount: float) -> None:
        self.deposit_transaction_repository.create_transaction(balance_id, amount)

    def get_transaction_history(self, balance_id: uuid.UUID) -> list[Transaction]:
        ml_request_transactions = (
            self.ml_request_transaction_repository.get_all_transactions(balance_id)
        )
        deposit_transactions = self.deposit_transaction_repository.get_all_transactions(
            balance_id
        )
        all_transactions = ml_request_transactions + deposit_transactions

        all_transactions.sort(key=lambda t: t.timestamp, reverse=True)
        return all_transactions
