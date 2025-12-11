from abc import ABC, abstractmethod
import uuid

from entities.transaction.transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def get_all_transactions(self, balance_id: uuid.UUID) -> list[Transaction]:
        raise NotImplementedError
