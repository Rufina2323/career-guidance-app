from uuid import uuid4
from unittest.mock import patch

from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from services.response_data_service import ResponseDataService


def test_add_data(response_data_service: ResponseDataService) -> None:
    response_data = CareerPredictionModelResponseData(job_role_result="Engineer")
    response_data_id = uuid4()

    with patch.object(
        response_data_service.response_data_repository,
        "add_data",
        return_value=response_data_id,
    ) as mock_add_data:
        result = response_data_service.add_data(response_data_id, response_data)

        mock_add_data.assert_called_once_with(response_data_id, response_data)
        assert result == response_data_id
