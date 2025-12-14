import uuid
from abc import abstractmethod

from repositories.transaction.repository import TransactionRepository


class DepositTransactionRepository(TransactionRepository):
    @abstractmethod
    def create_transaction(self, balance_id: uuid.UUID, amount: float) -> None:
        raise NotImplementedError
