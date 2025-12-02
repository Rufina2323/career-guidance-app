from dataclasses import dataclass

from entities.person.person import Person


@dataclass
class User(Person):
    pass
