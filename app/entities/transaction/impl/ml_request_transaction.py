from dataclasses import dataclass

from entities.ml_request import MLRequest
from entities.transaction.transaction import Transaction


@dataclass
class MLRequestTransaction(Transaction):
    ml_request: MLRequest
