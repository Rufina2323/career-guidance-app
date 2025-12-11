from abc import ABC, abstractmethod
import uuid

from entities.response_data.response_data import ResponseData


class ResponseDataRepository(ABC):
    @abstractmethod
    def add_data(self, response_data: ResponseData) -> uuid.UUID:
        raise NotImplementedError

    @abstractmethod
    def get_data(self, response_data_id: uuid.UUID) -> ResponseData | None:
        raise NotImplementedError
