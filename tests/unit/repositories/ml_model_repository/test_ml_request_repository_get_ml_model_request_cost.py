from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlmodel import select
from sqlalchemy.exc import NoResultFound

from repositories.ml_model.impl.ml_model_psql_repository import MLModelPSQLRepository
from models.ml_model import MLModel as MLModelModel


def test_get_ml_model_request_cost_success(
    ml_model_psql_repository: MLModelPSQLRepository,
) -> None:
    ml_model_id = uuid4()

    with patch.object(ml_model_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session

        mock_psql_model = MagicMock()
        mock_psql_model.request_cost = 25.0
        mock_session.exec.return_value.one.return_value = mock_psql_model

        result = ml_model_psql_repository.get_ml_model_request_cost(ml_model_id)

        expected_statement = select(MLModelModel).where(MLModelModel.id == ml_model_id)
        used_statement = mock_session.exec.call_args.args[0]

        assert expected_statement.compare(used_statement)
        assert result == 25.0


def test_get_ml_model_request_cost_not_found(
    ml_model_psql_repository: MLModelPSQLRepository,
) -> None:
    ml_model_id = uuid4()

    with patch.object(ml_model_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session
        mock_session.exec.return_value.one.side_effect = NoResultFound

        result = ml_model_psql_repository.get_ml_model_request_cost(ml_model_id)

        assert result is None
