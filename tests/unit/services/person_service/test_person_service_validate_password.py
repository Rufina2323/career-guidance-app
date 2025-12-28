import pytest

from services.user_service import UserService


@pytest.mark.parametrize(
    "password, expected_errors",
    [
        ("Short1!", ["Password must be at least 8 characters long."]),
        ("nouppercase1!", ["Password must contain at least one uppercase letter."]),
        ("NOLOWERCASE1!", ["Password must contain at least one lowercase letter."]),
        ("NoDigits!", ["Password must contain at least one digit."]),
        (
            "NoSpecial1",
            ["Password must contain at least one special character (!@#$%^&* etc)."],
        ),
        ("Vaalid1!", []),
    ],
)
def test_validate_password(user_service: UserService, password, expected_errors):
    errors = user_service.validate_password(password)
    assert errors == expected_errors
