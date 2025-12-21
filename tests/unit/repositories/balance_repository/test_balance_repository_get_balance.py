from uuid import uuid4
from unittest.mock import MagicMock, patch

from sqlmodel import select
from sqlalchemy.exc import NoResultFound

from models.balance import Balance
from repositories.balance.impl.balance_psql_repository import BalancePSQLRepository


def test_get_balance_success(balance_psql_repository: BalancePSQLRepository) -> None:
    balance_id = uuid4()

    with patch.object(balance_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session

        mock_psql_balance = MagicMock()
        mock_psql_balance.amount = 500.0
        mock_session.exec.return_value.one.return_value = mock_psql_balance

        result = balance_psql_repository.get_balance(balance_id)

        expected_statement = select(Balance).where(Balance.id == balance_id)
        used_statement = mock_session.exec.call_args.args[0]

        assert expected_statement.compare(used_statement)
        assert result is not None
        assert result.amount == 500.0


def test_get_balance_not_found(balance_psql_repository: BalancePSQLRepository) -> None:
    balance_id = uuid4()

    with patch.object(balance_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session

        mock_session.exec.return_value.one.side_effect = NoResultFound

        result = balance_psql_repository.get_balance(balance_id)

        assert result is None
