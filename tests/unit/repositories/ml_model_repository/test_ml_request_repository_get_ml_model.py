from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlalchemy.exc import NoResultFound

from repositories.ml_model.impl.ml_model_psql_repository import MLModelPSQLRepository


def test_get_ml_model_not_found(
    ml_model_psql_repository: MLModelPSQLRepository,
) -> None:
    ml_model_id = uuid4()

    with patch.object(ml_model_psql_repository, "session_maker") as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session
        mock_session.exec.return_value.one.side_effect = NoResultFound

        result = ml_model_psql_repository.get_ml_model(ml_model_id)

        assert result is None
