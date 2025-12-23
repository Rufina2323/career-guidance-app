from uuid import uuid4
from services.user_service import UserService


def test_get_user_balance_id(user_service: UserService):
    person_id = uuid4()
    balance_id = uuid4()
    user_service.person_repository.get_user_balance_id.return_value = balance_id

    result = user_service.get_user_balance_id(person_id)
    assert result == balance_id
