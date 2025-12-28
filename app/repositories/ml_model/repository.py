from abc import ABC, abstractmethod
import uuid

from entities.ml_model.ml_model import MLModel


class MLModelRepository(ABC):
    @abstractmethod
    def get_all_ml_models(self) -> list[MLModel]:
        raise NotImplementedError

    @abstractmethod
    def get_ml_model_request_cost(self, ml_model_id: uuid.UUID) -> float | None:
        raise NotImplementedError

    @abstractmethod
    def get_ml_model(self, ml_model_id: uuid.UUID) -> MLModel:
        raise NotImplementedError
