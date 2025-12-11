from abc import abstractmethod
import uuid
from entities.transaction.transaction import Transaction
from repositories.transaction.repository import TransactionRepository


class TransactionPSQLRepository(TransactionRepository):
    @abstractmethod
    def get_all_transactions(self, balance_id: uuid.UUID) -> list[Transaction]:
        raise NotImplementedError
