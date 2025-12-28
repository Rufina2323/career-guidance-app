from uuid import uuid4
from unittest.mock import patch

import pytest

from services.admin_service import AdminService


def test_deposit_to_user(admin_service: AdminService) -> None:
    person_id = uuid4()
    amount = 100
    balance_id = uuid4()

    with (
        patch.object(admin_service, "get_user_balance_id") as mock_get_user_balance_id,
        patch.object(
            admin_service.balance_service, "deposit"
        ) as mock_balance_service_deposit,
    ):
        mock_get_user_balance_id.return_value = balance_id

        admin_service.deposit_to_user(person_id, amount)

        mock_balance_service_deposit.assert_called_once_with(balance_id, amount)


def test_deposit_to_user_balance_not_found(admin_service: AdminService) -> None:
    person_id = uuid4()
    amount = 100

    with (
        patch.object(admin_service, "get_user_balance_id") as mock_get_user_balance_id,
        patch.object(
            admin_service.balance_service, "deposit"
        ) as mock_balance_service_deposit,
    ):
        mock_get_user_balance_id.return_value = None

        with pytest.raises(ValueError):
            admin_service.deposit_to_user(person_id, amount)
