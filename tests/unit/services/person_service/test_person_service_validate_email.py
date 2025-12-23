import pytest

from services.user_service import UserService


@pytest.mark.parametrize(
    "email, expected_errors",
    [
        ("user@example.com", []),
        ("invalid-email", ["Invalid email format."]),
        ("user@.com", ["Invalid email format."]),
    ],
)
def test_validate_email(user_service: UserService, email, expected_errors):
    errors = user_service.validate_email(email)
    assert errors == expected_errors
