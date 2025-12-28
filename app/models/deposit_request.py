from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.person import Person


class DepositStatus(str, Enum):
    QUEUED = "queued"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"


class DepositRequest(SQLModel, table=True):
    __tablename__ = "deposit_request"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    amount: float
    deposit_status: DepositStatus
    timestamp: datetime
    person_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("person.id", name="fk_person_id"))
    )

    person: "Person" = Relationship(back_populates="deposit_requests")
