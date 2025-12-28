from uuid import uuid4
from entities.balance import Balance
from entities.person.impl.user import User

from services.user_service import UserService


def test_validate_username_exists(user_service: UserService):
    username = "existing_user"
    user_service.person_repository.get_by_username.return_value = User(
        user_id=uuid4(),
        username=username,
        email="a@b.com",
        password_hash="hash",
        balance=Balance(amount=100),
    )

    errors = user_service.validate_username(username)
    assert errors == ["This username exists."]


def test_validate_username_not_exists(user_service: UserService):
    username = "new_user"
    user_service.person_repository.get_by_username.return_value = None

    errors = user_service.validate_username(username)
    assert errors == []
