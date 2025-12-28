from datetime import datetime
import uuid
from pydantic import BaseModel


class DepositRequestDTO(BaseModel):
    deposit_id: uuid.UUID
    amount: float
    timestamp: datetime
    username: str
