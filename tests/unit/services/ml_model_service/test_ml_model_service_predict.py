from uuid import uuid4
from unittest.mock import patch, MagicMock
from entities.ml_model.impl.career_prediction_model import CareerPredictionModel
import torch

from services.ml_model_service import MLModelService

def test_predict(ml_model_service: MLModelService) -> None:
    ml_model_id = uuid4()
    response_data_id = uuid4()
    inference_data = {"feature1": 1, "feature2": 2}

    # Create MLModel mock
    mock_ml_model = MagicMock(spec=CareerPredictionModel)

    # Manually add the attributes used in predict
    mock_ml_model.preprocessing_pipeline = MagicMock()
    mock_ml_model.preprocessing_pipeline.transform.return_value.toarray.return_value = [[0.1, 0.2]]

    mock_ml_model.model = MagicMock(return_value=torch.tensor([[0.1, 0.9]]))
    mock_ml_model.label_encoder = MagicMock()
    mock_ml_model.label_encoder.inverse_transform.return_value = ["Engineer"]

    with patch.object(ml_model_service, "get_ml_model", return_value=mock_ml_model), \
         patch.object(ml_model_service.response_data_service, "add_data", return_value=response_data_id) as mock_add_data:

        result = ml_model_service.predict(ml_model_id, response_data_id, inference_data)

        ml_model_service.get_ml_model.assert_called_once_with(ml_model_id)

        mock_ml_model.preprocessing_pipeline.transform.assert_called_once()
        mock_ml_model.model.assert_called_once()
        mock_ml_model.label_encoder.inverse_transform.assert_called_once()

        mock_add_data.assert_called_once()
        assert result == response_data_id
