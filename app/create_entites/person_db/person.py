from abc import ABC
from dataclasses import dataclass


@dataclass
class PersonDBCreateEntity(ABC):
    username: str
    email: str
    password_hash: str
