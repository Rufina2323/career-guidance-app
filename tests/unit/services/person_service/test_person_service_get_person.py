from uuid import uuid4
from entities.balance import Balance
from entities.person.impl.user import User
from services.user_service import UserService


def test_get_person(user_service: UserService):
    person_id = uuid4()
    person = User(user_id=uuid4(), username="user", email="a@b.com", password_hash="hash", balance=Balance(amount=100))
    user_service.person_repository.get_person.return_value = person

    result = user_service.get_person(person_id)
    assert result == person
