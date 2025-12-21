from uuid import uuid4
from unittest.mock import patch
import pytest
from entities.balance import Balance

from services.balance_service import BalanceService


def test_can_withdraw_success(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    balance = Balance(amount=100.0)

    with patch.object(
        balance_service,
        "get_balance",
        return_value=balance,
    ):
        # should not raise
        balance_service.can_withdraw(balance_id, 50.0)


def test_can_withdraw_invalid_amount(balance_service: BalanceService) -> None:
    balance_id = uuid4()

    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        balance_service.can_withdraw(balance_id, -10)

    
def test_can_withdraw_balance_not_found(balance_service: BalanceService) -> None:
    balance_id = uuid4()

    with patch.object(
        balance_service,
        "get_balance",
        return_value=None,
    ):
        with pytest.raises(ValueError, match="Balance does not exist"):
            balance_service.can_withdraw(balance_id, 10)


def test_can_withdraw_insufficient_balance(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    balance = Balance(amount=20.0)

    with patch.object(
        balance_service,
        "get_balance",
        return_value=balance,
    ):
        with pytest.raises(ValueError, match="Insufficient balance"):
            balance_service.can_withdraw(balance_id, 50)


