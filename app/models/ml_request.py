from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from sqlalchemy import ForeignKey, Column, UUID as SA_UUID

if TYPE_CHECKING:
    from models.inference_data import InferenceData
    from models.person import Person
    from models.ml_request_transaction import MLRequestTransaction
    from models.response_data import ResponseData
    from models.ml_model import MLModel


class MLRequest(SQLModel, table=True):
    __tablename__ = "ml_request"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str
    timestamp: datetime
    credits_used: float = Field(default=0.0)

    user_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("person.id", name="fk_person_id"))
    )
    ml_model_id: uuid.UUID = Field(
        sa_column=Column(SA_UUID, ForeignKey("ml_model.id", name="fk_ml_model_id"))
    )
    inference_data_id: uuid.UUID = Field(
        sa_column=Column(
            SA_UUID, ForeignKey("inference_data.id", name="fk_inference_data_id")
        )
    )

    response_data_id: uuid.UUID = Field(
        sa_column=Column(
            SA_UUID, ForeignKey("response_data.id", name="fk_response_data_id")
        )
    )

    person: "Person" = Relationship(back_populates="ml_requests")
    ml_model: "MLModel" = Relationship(back_populates="ml_requests")
    inference_data: "InferenceData" = Relationship(back_populates="ml_request")
    response_data: "ResponseData" = Relationship(back_populates="ml_request")
    ml_request_transaction: "MLRequestTransaction" = Relationship(
        back_populates="ml_request"
    )
