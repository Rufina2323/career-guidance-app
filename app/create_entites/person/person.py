from abc import ABC
from dataclasses import dataclass


@dataclass
class PersonCreateEntity(ABC):
    username: str
    email: str
    password: str
