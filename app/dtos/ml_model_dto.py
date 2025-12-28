import uuid
from pydantic import BaseModel


class MLModelDTO(BaseModel):
    id: uuid.UUID
    name: str
    cost: float
