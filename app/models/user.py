from models.balance import Balance
from sqlmodel import SQLModel, Field, Relationship

import uuid

from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: Role = Field(default=Role.USER)
    balance_id: uuid.UUID = Field(foreign_key="balance.id")

    balance: Balance = Relationship(back_populates="user")
    