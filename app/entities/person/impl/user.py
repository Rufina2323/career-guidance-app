from dataclasses import dataclass

from entities.person.person import Person


@dataclass
class User(Person):
    def check_password(self, password_hash: str) -> bool:
        pass

    def get_balance(self) -> float:
        pass
