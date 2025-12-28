from abc import ABC
from dataclasses import dataclass, field

from datetime import datetime
from entities.balance import Balance


@dataclass
class Transaction(ABC):
    balance: Balance
    amount: float
    timestamp: datetime
