from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.data import Data
    from models.user import User
    from models.ml_model import MLModel


class MLRequest(SQLModel, table=True):
    __tablename__ = "ml_request"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str
    timestamp: datetime
    credits_used: float = Field(default=0.0)

    user_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("user.id", name="fk_user_id"))
    )
    ml_model_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("ml_model.id", name="fk_ml_model_id"))
    )
    data_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("data.id", name="fk_ml_data_id"))
    )

    user: "User" = Relationship(back_populates="ml_request")
    ml_model: "MLModel" = Relationship(back_populates="ml_request")
    data: "Data" = Relationship(back_populates="ml_request")
