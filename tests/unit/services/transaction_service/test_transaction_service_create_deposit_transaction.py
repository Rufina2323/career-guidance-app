from uuid import uuid4
from unittest.mock import patch

from services.transaction_service import TransactionService


def test_create_deposit_transaction(transaction_service: TransactionService) -> None:
    balance_id = uuid4()
    amount = 100.0

    with patch.object(
        transaction_service.deposit_transaction_repository, "create_transaction"
    ) as mock_create:
        transaction_service.create_deposit_transaction(balance_id, amount)
        mock_create.assert_called_once_with(balance_id, amount)
