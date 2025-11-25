from dataclasses import dataclass

from entities.transaction.transaction import Transaction


@dataclass
class DepositTransaction(Transaction):
    pass
