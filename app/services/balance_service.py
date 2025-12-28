import uuid
from entities.balance import Balance
from repositories.balance.impl.balance_psql_repository import BalancePSQLRepository
from repositories.balance.repository import BalanceRepository
from services.transaction_service import TransactionService


class BalanceService:
    def __init__(self) -> None:
        self.transaction_service = TransactionService()
        self.balance_repository: BalanceRepository = BalancePSQLRepository()

    def deposit(self, balance_id: uuid.UUID, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance_repository.deposit(balance_id, amount)

        self.transaction_service.create_deposit_transaction(balance_id, amount)

    def get_balance(self, balance_id: uuid.UUID) -> Balance | None:
        balance = self.balance_repository.get_balance(balance_id)
        return balance

    def can_withdraw(self, balance_id: uuid.UUID, amount: float) -> tuple[bool, str]:
        if amount <= 0:
            return (False, "Withdrawal amount must be positive.")
        balance = self.get_balance(balance_id)
        if not balance:
            return (False, "Balance does not exist.")
        if amount > balance.amount:
            return (False, "Insufficient balance.")
        return (True, "Amount can be withdraw from balance.")

    def withdraw(
        self, ml_request_id: uuid.UUID, balance_id: uuid.UUID, amount: float
    ) -> None:
        self.balance_repository.withdraw(balance_id, amount)
        self.transaction_service.create_ml_request_transaction(
            ml_request_id, balance_id, amount
        )
