from dataclasses import dataclass

from create_entites.person_db.person import PersonDBCreateEntity


@dataclass
class AdminDBCreateEntity(PersonDBCreateEntity):
    pass
