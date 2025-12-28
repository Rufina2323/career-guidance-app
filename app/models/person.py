from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from . import SQLModel

import uuid

from entities.person.impl.user import User as UserEntity
from entities.person.impl.admin import Admin as AdminEntity
from entities.person.person import Person as PersonEntity
from entities.balance import Balance as BalanceEntity

from enum import Enum
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.balance import Balance
    from models.ml_request import MLRequest
    from models.deposit_request import DepositRequest


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Person(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    password_hash: str
    role: Role = Field(default=Role.USER)
    balance_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("balance.id", name="fk_balance_id"))
    )

    balance: "Balance" = Relationship(back_populates="person")
    ml_requests: list["MLRequest"] = Relationship(back_populates="person")
    deposit_requests: list["DepositRequest"] = Relationship(back_populates="person")

    @classmethod
    def to_domain(cls, user_model: "Person") -> PersonEntity:
        if user_model.role == Role.USER:
            return UserEntity(
                user_id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                balance=BalanceEntity(amount=user_model.balance.amount),
            )

        if user_model.role == Role.ADMIN:
            return AdminEntity(
                user_id=user_model.id,
                username=user_model.username,
                email=user_model.email,
                password_hash=user_model.password_hash,
                balance=BalanceEntity(amount=user_model.balance.amount),
            )
