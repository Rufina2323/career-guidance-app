from entities.balance import Balance
from entities.transaction.transaction import Transaction
from services.transaction_service import TransactionService


class BalanceService:
    def __init__(self) -> None:
        self.transaction_service = TransactionService()

    def deposit(self, balance: Balance, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.amount += amount
        return self.transaction_service.create_transaction(balance, amount)

    def can_withdraw(self, balance: Balance, amount: float) -> bool:
        return 0 <= amount <= balance.amount

    def withdraw(self, balance: Balance, amount: float) -> Transaction:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > balance.amount:
            raise ValueError("Insufficient balance")
        balance.amount -= amount
