from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.response.response import Response


class MLModelService:
    def preprocess_inference_data(
        self, ml_model: MLModel, inference_data: InferenceData
    ) -> InferenceData:
        pass

    def predict(self, inference_data: InferenceData) -> Response:
        pass
