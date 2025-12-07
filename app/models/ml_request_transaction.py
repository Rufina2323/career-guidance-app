from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.balance import Balance


class MLRequestTransaction(SQLModel, table=True):
    __tablename__ = "ml_request_transaction"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    timestamp: datetime
    ml_request_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("ml_request.id", name="fk_ml_request_id"))
    )
    balance_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("balance.id", name="fk_balance_id"))
    )

    balance: "Balance" = Relationship(back_populates="ml_request_transactions")
