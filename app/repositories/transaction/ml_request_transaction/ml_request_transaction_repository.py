from abc import abstractmethod
import uuid
from repositories.transaction.repository import TransactionRepository


class MLRequestTransactionRepository(TransactionRepository):
    @abstractmethod
    def create_transaction(
        self, ml_request_id: uuid.UUID, balance_id: uuid.UUID, amount: float
    ) -> None:
        raise NotImplementedError
