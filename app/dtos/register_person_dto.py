from enum import Enum
from pydantic import BaseModel


class RegisterRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class RegisterPersonDTO(BaseModel):
    username: str
    password: str
    email: str
    role: RegisterRole
    