
from typing import TYPE_CHECKING
import uuid
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from models.ml_request import MLRequest


class MLModel(SQLModel, table=True):
    __tablename__ = "ml_model"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    request_cost: float
    model_path: str
    preprocessing_path: str

    ml_request: "MLRequest" = Relationship(back_populates="ml_model")