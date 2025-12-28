from abc import ABC, abstractmethod
import uuid

from entities.ml_request import MLRequest
from models.ml_request import Status


class MLRequestRepository(ABC):
    @abstractmethod
    def create_ml_request(
        self,
        model_cost: float,
        user_id: uuid.UUID,
        model_id: uuid.UUID,
        inference_data_id: uuid.UUID,
        repsonse_data_id: uuid.UUID,
    ) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def change_ml_request_status(
        self, ml_request_id: uuid.UUID, ml_request_status: Status
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_prediction_id(self, ml_request_id: uuid.UUID) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def get_ml_request_status(self, ml_request_id: uuid.UUID) -> Status:
        raise NotImplementedError

    @abstractmethod
    def get_ml_request_cost(self, ml_request_id: uuid.UUID) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_user_id(self, ml_request_id: uuid.UUID) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def get_ml_request_history(self, user_id: uuid.UUID) -> list[MLRequest]:
        raise NotImplementedError
