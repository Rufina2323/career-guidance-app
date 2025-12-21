from uuid import uuid4
from unittest.mock import patch, MagicMock

from sqlalchemy.exc import NoResultFound

from repositories.ml_model.impl.ml_model_psql_repository import MLModelPSQLRepository


# def test_get_ml_model_success(ml_model_psql_repository):
#     ml_model_id = uuid4()

#     mock_psql_model = MagicMock()
#     mock_psql_model.id = ml_model_id
#     mock_psql_model.name = "Career Predictor"
#     mock_psql_model.request_cost = 10.0
#     mock_psql_model.model_path = "app/ml_models/career_prediction_model/mlp_model.pt"
#     mock_psql_model.preprocessing_path = "app/ml_models/career_prediction_model/preprocessor.joblib"
#     mock_psql_model.label_encoder_path = "app/ml_models/career_prediction_model/label_encoder.joblib"

#     with patch.object(ml_model_psql_repository, "session_maker") as mock_session_maker, \
#          patch("entities.ml_model.impl.career_prediction_model.CareerPredictionModel") as MockCareerModel:

#         mock_session = MagicMock()
#         mock_session_maker.return_value.__enter__.return_value = mock_session
#         mock_session.exec.return_value.one.return_value = mock_psql_model

#         mock_instance = MagicMock()
#         MockCareerModel.return_value = mock_instance

#         result = ml_model_psql_repository.get_ml_model(ml_model_id)

#         MockCareerModel.assert_called_once_with(
#             model_id=ml_model_id,
#             name="Career Predictor",
#             request_cost=10.0,
#             model_path="app/ml_models/career_prediction_model/mlp_model.pt",
#             preprocessing_path="app/ml_models/career_prediction_model/preprocessor.joblib",
#             label_encoder_path="app/ml_models/career_prediction_model/label_encoder.joblib",
#         )

#         assert result == mock_instance


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
