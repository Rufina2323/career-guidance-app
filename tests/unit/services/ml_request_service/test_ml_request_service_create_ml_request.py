from uuid import uuid4
from unittest.mock import patch
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from services.ml_request_service import MLRequestService
from create_entites.inference_data.inference_data import InferenceDataCreateEntity


def test_create_ml_request(ml_request_service: MLRequestService) -> None:
    user_id = uuid4()
    balance_id = uuid4()
    model_id = uuid4()
    response_data_id = uuid4()
    inference_data = InferenceDataCreateEntity()

    model_cost = 50.0
    ml_request_id = uuid4()
    inference_data_id = uuid4()

    with (
        patch.object(
            ml_request_service.ml_model_service,
            "get_ml_model_request_cost",
            return_value=model_cost,
        ) as mock_get_cost,
        patch.object(
            ml_request_service.balance_service,
            "can_withdraw",
            return_value=(True, "Amount can be withdraw from balance."),
        ) as mock_can_withdraw,
        patch.object(
            ml_request_service.inference_data_service,
            "add_data",
            return_value=inference_data_id,
        ) as mock_add_inference_data,
        patch.object(
            ml_request_service.response_data_service, "add_data"
        ) as mock_add_response_data,
        patch.object(
            ml_request_service.ml_request_repository,
            "create_ml_request",
            return_value=ml_request_id,
        ) as mock_create_ml_request,
        patch.object(ml_request_service.balance_service, "withdraw") as mock_withdraw,
    ):
        result = ml_request_service.create_ml_request(
            user_id, balance_id, model_id, response_data_id, inference_data
        )

        mock_get_cost.assert_called_once_with(model_id)
        mock_can_withdraw.assert_called_once_with(balance_id, model_cost)
        mock_add_inference_data.assert_called_once_with(inference_data)
        mock_add_response_data.assert_called_once_with(
            response_data_id, CareerPredictionModelResponseData(job_role_result="")
        )
        mock_create_ml_request.assert_called_once_with(
            model_cost, user_id, model_id, inference_data_id, response_data_id
        )
        mock_withdraw.assert_called_once_with(ml_request_id, balance_id, model_cost)

        assert result == ml_request_id
