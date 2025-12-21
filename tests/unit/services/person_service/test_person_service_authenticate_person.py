from uuid import uuid4
from entities.balance import Balance
from entities.person.impl.user import User
import bcrypt
from services.user_service import UserService


def test_authenticate_person_success(user_service: UserService):
    password = "Password1!"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
    person = User(user_id=uuid4(), username="user", email="a@b.com", password_hash=hashed, balance=Balance(amount=100))
    user_service.person_repository.get_by_username.return_value = person

    result = user_service.authenticate_person("user", password)
    assert result == person

def test_authenticate_person_wrong_password(user_service: UserService):
    person = User(user_id=uuid4(), username="user", email="a@b.com", password_hash=bcrypt.hashpw("Password1!".encode(), bcrypt.gensalt()).decode("utf-8"), balance=Balance(amount=100))
    user_service.person_repository.get_by_username.return_value = person

    result = user_service.authenticate_person("user", "WrongPass1!")
    assert result is None

def test_authenticate_person_not_found(user_service: UserService):
    user_service.person_repository.get_by_username.return_value = None
    result = user_service.authenticate_person("user", "Password1!")
    assert result is None
