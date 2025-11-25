from entities.balance import Balance
from entities.person.impl.user import User
from entities.transaction.transaction import Transaction


class TransactionService:
    def create_transaction(self, balance: Balance, amount: float) -> Transaction:
        pass

    def get_transaction_history(self, user: User) -> list[Transaction]:
        pass
