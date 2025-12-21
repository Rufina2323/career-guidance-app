from uuid import uuid4
from unittest.mock import patch

from services.balance_service import BalanceService
from entities.balance import Balance


def test_get_balance(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    balance = Balance(amount=50.0)

    with patch.object(
        balance_service.balance_repository,
        "get_balance",
        return_value=balance,
    ) as mock_get_balance:
        result = balance_service.get_balance(balance_id)

        mock_get_balance.assert_called_once_with(balance_id)
        assert result == balance
