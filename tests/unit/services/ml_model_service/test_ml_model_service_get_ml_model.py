from uuid import uuid4
from unittest.mock import patch, MagicMock

from services.ml_model_service import MLModelService
from entities.ml_model.ml_model import MLModel


def test_get_ml_model(ml_model_service: MLModelService) -> None:
    ml_model_id = uuid4()
    ml_model = MagicMock(spec=MLModel)

    with patch.object(
        ml_model_service.ml_model_repository,
        "get_ml_model",
        return_value=ml_model,
    ) as mock_get_ml_model:
        result = ml_model_service.get_ml_model(ml_model_id)

        mock_get_ml_model.assert_called_once_with(ml_model_id)
        assert result == ml_model
