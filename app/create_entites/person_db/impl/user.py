from dataclasses import dataclass

from create_entites.person.person import PersonCreateEntity


@dataclass
class UserDBCreateEntity(PersonCreateEntity):
    pass
