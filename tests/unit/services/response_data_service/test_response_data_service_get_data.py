from uuid import uuid4
from unittest.mock import patch


from entities.response_data.impl.career_prediction_model_response_data import CareerPredictionModelResponseData
from services.response_data_service import ResponseDataService


def test_get_data(response_data_service: ResponseDataService) -> None:
    response_data_id = uuid4()
    response_data = CareerPredictionModelResponseData(
        job_role_result="Engineer"
    )

    with patch.object(
        response_data_service.response_data_repository,
        "get_data",
        return_value=response_data,
    ) as mock_get_data:
        result = response_data_service.get_data(response_data_id)

        mock_get_data.assert_called_once_with(response_data_id)
        assert result == response_data
