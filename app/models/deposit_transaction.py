from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.balance import Balance


class DepositTransaction(SQLModel, table=True):
    __tablename__ = "deposit_transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    timestamp: datetime
    balance_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("balance.id", name="fk_balance_id"))
    )

    balance: "Balance" = Relationship(back_populates="deposit_transactions")
