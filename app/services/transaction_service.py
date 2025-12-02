from entities.balance import Balance
from entities.person.impl.user import User
from entities.transaction.transaction import Transaction


class TransactionService:
    # def __init__(self) -> None:
    # self.transaction_repository: TransactionRepository =

    def create_transaction(self, balance: Balance, amount: float) -> Transaction:
        # business logic

        self.transaction_repository.create_transaction()

        pass

    def get_transaction_history(self, user: User) -> list[Transaction]:
        pass
