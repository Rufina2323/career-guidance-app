from dataclasses import dataclass

from create_entites.person.person import PersonCreateEntity


@dataclass
class UserCreateEntity(PersonCreateEntity):
    pass
