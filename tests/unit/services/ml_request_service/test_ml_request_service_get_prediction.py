from uuid import uuid4
from unittest.mock import patch
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from services.ml_request_service import MLRequestService


def test_get_prediction(ml_request_service: MLRequestService) -> None:
    ml_request_id = uuid4()
    response_data_id = uuid4()
    response_data = CareerPredictionModelResponseData(job_role_result="Engineer")

    with (
        patch.object(
            ml_request_service.ml_request_repository,
            "get_prediction_id",
            return_value=response_data_id,
        ) as mock_get_response_id,
        patch.object(
            ml_request_service.response_data_service,
            "get_data",
            return_value=response_data,
        ) as mock_get_data,
    ):
        result = ml_request_service.get_prediction(ml_request_id)

        mock_get_response_id.assert_called_once_with(ml_request_id)
        mock_get_data.assert_called_once_with(response_data_id)
        assert result == response_data
