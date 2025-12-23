from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlmodel import select
from sqlalchemy.exc import NoResultFound

from repositories.inference_data.impl.inference_data_psql_repository import (
    InferenceDataPSQLRepository,
)
from models.inference_data import InferenceData as InferenceDataModel
from entities.inference_data.inference_data import InferenceData


def test_get_data_success(
    inference_data_psql_repository: InferenceDataPSQLRepository,
) -> None:
    inference_data_id = uuid4()

    mock_psql_data = MagicMock(spec=InferenceDataModel)
    domain_data = MagicMock(spec=InferenceData)

    with patch.object(
        inference_data_psql_repository, "session_maker"
    ) as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session
        mock_session.exec.return_value.one.return_value = mock_psql_data

        with patch.object(
            InferenceDataModel, "to_domain", return_value=domain_data
        ) as mock_to_domain:
            result = inference_data_psql_repository.get_data(inference_data_id)

            expected_statement = select(InferenceDataModel).where(
                InferenceDataModel.id == inference_data_id
            )
            used_statement = mock_session.exec.call_args.args[0]

            assert expected_statement.compare(used_statement)
            mock_to_domain.assert_called_once_with(mock_psql_data)
            assert result == domain_data


def test_get_data_not_found(
    inference_data_psql_repository: InferenceDataPSQLRepository,
) -> None:
    inference_data_id = uuid4()

    with patch.object(
        inference_data_psql_repository, "session_maker"
    ) as mock_session_maker:
        mock_session = MagicMock()
        mock_session_maker.return_value.__enter__.return_value = mock_session
        mock_session.exec.return_value.one.side_effect = NoResultFound

        result = inference_data_psql_repository.get_data(inference_data_id)

        assert result is None
