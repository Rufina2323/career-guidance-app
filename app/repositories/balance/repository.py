from abc import ABC, abstractmethod
import uuid

from entities.balance import Balance


class BalanceRepository(ABC):
    @abstractmethod
    def get_balance(self, balance_id: uuid.UUID) -> Balance | None:
        raise NotImplementedError

    @abstractmethod
    def deposit(self, balance_id: uuid.UUID, amount: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def withdraw(self, balance_id: uuid.UUID, amount: float) -> None:
        raise NotImplementedError
