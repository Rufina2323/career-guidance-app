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
        can_withdraw_result = balance_service.can_withdraw(balance_id, 50.0)
        assert can_withdraw_result == (True, "Amount can be withdraw from balance.")


def test_can_withdraw_invalid_amount(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    result = balance_service.can_withdraw(balance_id, -10)
    assert result == (False, "Withdrawal amount must be positive.")


def test_can_withdraw_balance_not_found(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    with patch.object(balance_service, "get_balance", return_value=None):
        result = balance_service.can_withdraw(balance_id, 10)
        assert result == (False, "Balance does not exist.")


def test_can_withdraw_insufficient_balance(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    balance = Balance(amount=20.0)
    with patch.object(balance_service, "get_balance", return_value=balance):
        result = balance_service.can_withdraw(balance_id, 50)
        assert result == (False, "Insufficient balance.")
