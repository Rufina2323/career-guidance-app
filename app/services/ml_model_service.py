import uuid
from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)


class MLModelService:
    def get_model_cost(self, model_id: uuid.UUID) -> float:
        return 100

    def preprocess_inference_data(
        self, ml_model: MLModel, inference_data: InferenceData
    ) -> InferenceData:
        pass

    def predict(
        self, ml_model_id: uuid.UUID, inference_data: InferenceData
    ) -> CareerPredictionModelResponseData:
        return CareerPredictionModelResponseData(job_role_result="None")
