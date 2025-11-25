from abc import ABC, abstractmethod
from dataclasses import dataclass

from entities.balance import Balance


@dataclass
class Person(ABC):
    user_id: int
    username: str
    email: str
    password_hash: str
    balance: Balance

    @abstractmethod
    def check_password(self, password_hash: str) -> bool:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass
