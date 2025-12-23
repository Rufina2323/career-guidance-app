from uuid import uuid4
from unittest.mock import patch

from services.balance_service import BalanceService


def test_withdraw_success(balance_service: BalanceService) -> None:
    ml_request_id = uuid4()
    balance_id = uuid4()
    amount = 30.0

    with (
        patch.object(
            balance_service.balance_repository,
            "withdraw",
        ) as mock_repo_withdraw,
        patch.object(
            balance_service.transaction_service,
            "create_ml_request_transaction",
        ) as mock_create_transaction,
    ):
        balance_service.withdraw(ml_request_id, balance_id, amount)

        mock_repo_withdraw.assert_called_once_with(balance_id, amount)
        mock_create_transaction.assert_called_once_with(
            ml_request_id, balance_id, amount
        )
