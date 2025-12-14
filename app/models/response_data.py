from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid

if TYPE_CHECKING:
    from models.ml_request import MLRequest


class ResponseData(SQLModel, table=True):
    __tablename__ = "response_data"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    job_role_result: str

    ml_request: "MLRequest" = Relationship(back_populates="response_data")
