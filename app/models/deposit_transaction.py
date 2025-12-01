from datetime import datetime
from models.balance import Balance
from sqlmodel import SQLModel, Field, Relationship
import uuid


class DepositTransaction(SQLModel, table=True):
    __tablename__ = "deposit_transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    timestamp: datetime
    balance_id: uuid.UUID = Field(foreign_key="balance.id")

    balance: Balance = Relationship(back_populates="deposit_transactions")
