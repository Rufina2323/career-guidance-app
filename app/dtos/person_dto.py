import uuid
from pydantic import BaseModel


class PersonDTO(BaseModel):
    user_id: uuid.UUID
    username: str
    role: str
