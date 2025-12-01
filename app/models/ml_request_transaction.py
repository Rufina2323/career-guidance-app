from datetime import datetime
from models.balance import Balance
from sqlmodel import SQLModel, Field, Relationship
import uuid


class MLRequestTransaction(SQLModel, table=True):
    __tablename__ = "ml_request_transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    timestamp: datetime
    ml_request_id: uuid.UUID = Field(foreign_key="ml_request.id")
    balance_id: uuid.UUID = Field(foreign_key="balance.id")

    balance: Balance = Relationship(back_populates="ml_request_transactions")
