from uuid import uuid4
from unittest.mock import patch

import pytest

from services.balance_service import BalanceService


def test_deposit_success(balance_service: BalanceService) -> None:
    balance_id = uuid4()
    amount = 100.0

    with (
        patch.object(balance_service.balance_repository, "deposit") as mock_repo_deposit,
        patch.object(
            balance_service.transaction_service,
            "create_deposit_transaction",
        ) as mock_create_transaction,
    ):
        balance_service.deposit(balance_id, amount)

        mock_repo_deposit.assert_called_once_with(balance_id, amount)
        mock_create_transaction.assert_called_once_with(balance_id, amount)


def test_deposit_invalid_amount(balance_service: BalanceService) -> None:
    balance_id = uuid4()

    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        balance_service.deposit(balance_id, 0)
