from uuid import uuid4
from unittest.mock import patch, MagicMock

from services.transaction_service import TransactionService
from entities.transaction.transaction import Transaction


def test_get_transaction_history(transaction_service: TransactionService) -> None:
    balance_id = uuid4()

    # Create mock transactions
    t1 = MagicMock(spec=Transaction)
    t2 = MagicMock(spec=Transaction)
    t3 = MagicMock(spec=Transaction)
    t1.timestamp = 10
    t2.timestamp = 20
    t3.timestamp = 15

    with patch.object(transaction_service.ml_request_transaction_repository, "get_all_transactions", return_value=[t1, t2]) as mock_ml, \
         patch.object(transaction_service.deposit_transaction_repository, "get_all_transactions", return_value=[t3]) as mock_deposit:

        result = transaction_service.get_transaction_history(balance_id)

        mock_ml.assert_called_once_with(balance_id)
        mock_deposit.assert_called_once_with(balance_id)

        # Transactions should be sorted by timestamp descending
        assert result == [t2, t3, t1]
