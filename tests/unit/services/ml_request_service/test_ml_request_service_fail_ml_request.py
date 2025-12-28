from uuid import uuid4
from unittest.mock import patch
from services.ml_request_service import MLRequestService


def test_fail_ml_request(ml_request_service: MLRequestService) -> None:
    ml_request_id = uuid4()
    user_id = uuid4()
    balance_id = uuid4()
    model_cost = 30.0

    with (
        patch.object(
            ml_request_service.ml_request_repository,
            "get_user_id",
            return_value=user_id,
        ) as mock_get_user_id,
        patch.object(
            ml_request_service.user_service,
            "get_user_balance_id",
            return_value=balance_id,
        ) as mock_get_balance_id,
        patch.object(
            ml_request_service.ml_request_repository,
            "get_ml_request_cost",
            return_value=model_cost,
        ) as mock_get_cost,
        patch.object(ml_request_service.balance_service, "deposit") as mock_deposit,
    ):
        ml_request_service.fail_ml_request(ml_request_id)

        mock_get_user_id.assert_called_once_with(ml_request_id)
        mock_get_balance_id.assert_called_once_with(user_id)
        mock_get_cost.assert_called_once_with(ml_request_id)
        mock_deposit.assert_called_once_with(balance_id, model_cost)
