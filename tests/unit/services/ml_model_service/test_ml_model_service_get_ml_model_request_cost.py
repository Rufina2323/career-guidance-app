from uuid import uuid4
from unittest.mock import patch

from services.ml_model_service import MLModelService


def test_get_ml_model_request_cost(ml_model_service: MLModelService) -> None:
    ml_model_id = uuid4()
    cost = 12.5

    with patch.object(
        ml_model_service.ml_model_repository,
        "get_ml_model_request_cost",
        return_value=cost,
    ) as mock_get_cost:
        result = ml_model_service.get_ml_model_request_cost(ml_model_id)

        mock_get_cost.assert_called_once_with(ml_model_id)
        assert result == cost
