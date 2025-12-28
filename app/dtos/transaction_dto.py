from datetime import datetime
from pydantic import BaseModel


class TransactionDTO(BaseModel):
    transaction_type: str
    amount: float
    timestamp: datetime
