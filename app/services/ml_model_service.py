import uuid
from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from repositories.ml_model.impl.ml_model_psql_repository import MLModelPSQLRepository
from repositories.ml_model.repository import MLModelRepository
from services.response_data_service import ResponseDataService
import torch
import pandas as pd


class MLModelService:
    def __init__(self) -> None:
        self.response_data_service = ResponseDataService()
        self.ml_model_repository: MLModelRepository = MLModelPSQLRepository()

    def get_ml_model_request_cost(self, ml_model_id: uuid.UUID) -> float:
        return self.ml_model_repository.get_ml_model_request_cost(ml_model_id)

    def get_ml_model(self, ml_model_id: uuid.UUID) -> MLModel:
        return self.ml_model_repository.get_ml_model(ml_model_id)

    def predict(
        self,
        ml_model_id: uuid.UUID,
        repsonse_data_id: uuid.UUID,
        inference_data: InferenceData,
    ) -> uuid.UUID:
        ml_model = self.get_ml_model(ml_model_id)
        inference_data["instrovert"] = "yes" if True else "no"
        print(inference_data)
        inference_data_df = pd.DataFrame([inference_data])
        preprocessed_data = ml_model.preprocessing_pipeline.transform(
            inference_data_df
        ).toarray()
        preprocessed_data_tensor = torch.tensor(preprocessed_data, dtype=torch.float32)
        with torch.no_grad():
            logits = ml_model.model(preprocessed_data_tensor)
            preds = torch.argmax(logits, dim=1)

        predicted_labels = ml_model.label_encoder.inverse_transform(preds.numpy())
        prediction = CareerPredictionModelResponseData(
            job_role_result=predicted_labels[0]
        )
        repsonse_data_id = self.response_data_service.add_data(
            repsonse_data_id, prediction
        )
        return repsonse_data_id
