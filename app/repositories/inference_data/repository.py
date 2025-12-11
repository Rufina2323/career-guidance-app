from abc import ABC, abstractmethod
import uuid

from create_entites.inference_data.inference_data import InferenceDataCreateEntity
from entities.inference_data.inference_data import InferenceData


class InferenceDataRepository(ABC):
    @abstractmethod
    def add_data(self, inference_data: InferenceDataCreateEntity) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def get_data(self, inference_data_id: uuid.UUID) -> InferenceData | None:
        raise NotImplementedError
