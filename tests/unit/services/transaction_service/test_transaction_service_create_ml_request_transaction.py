from uuid import uuid4
from unittest.mock import patch

from services.transaction_service import TransactionService


def test_create_ml_request_transaction(transaction_service: TransactionService) -> None:
    ml_request_id = uuid4()
    balance_id = uuid4()
    amount = 50.0

    with patch.object(transaction_service.ml_request_transaction_repository, "create_transaction") as mock_create:
        transaction_service.create_ml_request_transaction(ml_request_id, balance_id, amount)
        mock_create.assert_called_once_with(ml_request_id, balance_id, amount)
