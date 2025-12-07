from abc import ABC
from dataclasses import dataclass
import uuid

from entities.balance import Balance


@dataclass
class Person(ABC):
    user_id: uuid.UUID
    username: str
    email: str
    password_hash: str
    balance: Balance
