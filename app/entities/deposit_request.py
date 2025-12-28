from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class DepositRequest:
    deposit_id: uuid.UUID
    amount: float
    deposit_status: str
    timestamp: datetime
    person_id: uuid.UUID
