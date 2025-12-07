from abc import ABC
import uuid
import bcrypt
import re

from create_entites.person.person import PersonCreateEntity
from create_entites.person_db.person import PersonDBCreateEntity
from entities.balance import Balance
from entities.person.person import Person
from repositories.person.repository import PersonRepository
from services.balance_service import BalanceService


class PersonService(ABC):
    def __init__(self) -> None:
        self.balance_service = BalanceService()

        self.person_repository: PersonRepository

    def validate_password(self, password: str) -> list[str]:
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character (!@#$%^&* etc).")

        return errors

    def validate_email(self, email: str) -> list[str]:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return ["Invalid email format."]
        return []
    
    def validate_username(self, username: str) -> list[str]:
        person = self.person_repository.get_by_username(username)
        if person:
            return ["This username exists."]
        return []

    def get_person(self, person_id: uuid.UUID) -> Person | None:
        return self.person_repository.get_person(person_id)
    
    def authenticate_person(self, username: str, raw_password: str) -> Person | None:
        person = self.person_repository.get_by_username(username)
        if not person:
            return None
        print(person)
        print(len(person.password_hash))
        print(bcrypt.hashpw(
            raw_password.encode(), bcrypt.gensalt()
        ))
        if not bcrypt.checkpw(raw_password.encode(), person.password_hash.encode('utf-8')):
            return None

        return person

    def add_person(self, person_create_entity: PersonCreateEntity) -> tuple[bool, list[str] | Person]:
        errors = []

        errors.extend(self.validate_username(person_create_entity.username))
        errors.extend(self.validate_email(person_create_entity.email))
        errors.extend(self.validate_password(person_create_entity.password))
        if errors:
            return False, errors
        
        password_hash = bcrypt.hashpw(
            person_create_entity.password.encode(), bcrypt.gensalt()
        ).decode('utf-8')
        person_db_create_entity = PersonDBCreateEntity(
            username=person_create_entity.username,
            email=person_create_entity.email,
            password_hash=password_hash
        )
        person = self.person_repository.add_person(person_db_create_entity)
        return True, person

    def get_balance(self, person_id: uuid.UUID) -> Balance:
        person = self.person_repository.get_person(person_id)
        if person:
            return person.balance
        return None
