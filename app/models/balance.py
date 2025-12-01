from models.deposit_transaction import DepositTransaction
from models.ml_request_transaction import MLRequestTransaction
from models.user import User
from sqlmodel import SQLModel, Field, Relationship

import uuid


class Balance(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float = Field(default=0.0)

    user: User = Relationship(back_populates="balance")
    deposit_transactions: list[DepositTransaction] = Relationship(back_populates="balance")
    ml_request_transactions: list[MLRequestTransaction] = Relationship(back_populates="balance")
    