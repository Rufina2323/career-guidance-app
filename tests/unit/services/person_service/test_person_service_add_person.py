from uuid import uuid4
from entities.balance import Balance
from entities.person.impl.user import User
from services.user_service import UserService
from create_entites.person.impl.user import UserCreateEntity


def test_add_person_success(user_service: UserService):
    user_service.person_repository.get_by_username.return_value = None
    person_create = UserCreateEntity(username="user", email="a@b.com", password="Password1!")
    mock_person = User(user_id=uuid4(), username="user", email="a@b.com", password_hash="hash", balance=Balance(amount=100))
    user_service.person_repository.add_person.return_value = mock_person

    success, result = user_service.add_person(person_create)
    assert success is True
    assert result == mock_person

def test_add_person_validation_error(user_service: UserService):
    user_service.person_repository.get_by_username.return_value = User(user_id=uuid4(), username="user", email="a@b.com", password_hash="hash", balance=Balance(amount=100))
    person_create = UserCreateEntity(username="user", email="invalid-email", password="short")
    success, errors = user_service.add_person(person_create)
    assert success is False
    assert "This username exists." in errors
    assert "Invalid email format." in errors
    assert "Password must be at least 8 characters long." in errors
