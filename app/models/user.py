from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from . import SQLModel

import uuid

from enum import Enum
if TYPE_CHECKING:
    from models.balance import Balance
    

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

from sqlalchemy import ForeignKey, Column, UUID as SA_UUID


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: Role = Field(default=Role.USER)
    balance_id: uuid.UUID = Field(sa_column=Column(SA_UUID, ForeignKey("balance.id", name="fk_balance_id")))

    balance: "Balance" = Relationship(back_populates="user")
