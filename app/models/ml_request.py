from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid

from models.data import Data
from models.ml_model import MLModel
from models.user import User


class MLRequest(SQLModel, table=True):
    __tablename__ = "ml_request"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str
    timestamp: datetime
    credits_used: float = Field(default=0.0)
    
    user_id: uuid.UUID = Field(foreign_key="user.id")
    ml_model_id: uuid.UUID = Field(foreign_key="ml_model.id")
    data_id: uuid.UUID = Field(foreign_key="data.id")

    user: User = Relationship(back_populates="ml_request")
    ml_model: MLModel = Relationship(back_populates="ml_request")
    data: Data = Relationship(back_populates="ml_request")
