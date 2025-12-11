from abc import ABC, abstractmethod
import uuid

from entities.ml_request import MLRequest


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
    def get_ml_request_history(self, user_id: uuid.UUID) -> list[MLRequest]:
        raise NotImplementedError
