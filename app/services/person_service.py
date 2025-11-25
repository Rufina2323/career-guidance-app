from abc import ABC

from services.balance_service import BalanceService


class PersonService(ABC):
    def __init__(self) -> None:
        self.balance_service = BalanceService()
