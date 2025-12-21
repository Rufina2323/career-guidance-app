from uuid import uuid4
from sqlmodel import select

from models.balance import Balance
from unittest.mock import patch, MagicMock

from repositories.balance.impl.balance_psql_repository import BalancePSQLRepository


def test_withdraw(balance_psql_repository: BalancePSQLRepository) -> None:
    balance_id = uuid4()
    amount = 300.0

    with patch.object(balance_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session

        mock_psql_balance = MagicMock()
        mock_psql_balance.amount = 1000.0
        mock_session.exec.return_value.one.return_value = mock_psql_balance

        balance_psql_repository.withdraw(balance_id, amount)

        expected_statement = select(Balance).where(Balance.id == balance_id)
        used_statement = mock_session.exec.call_args.args[0]

        assert expected_statement.compare(used_statement)
        assert mock_psql_balance.amount == 700.0
        mock_session.commit.assert_called_once()
