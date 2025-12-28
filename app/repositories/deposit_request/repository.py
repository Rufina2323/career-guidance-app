from abc import ABC, abstractmethod
import uuid

from entities.deposit_request import DepositRequest
from models.deposit_request import DepositStatus


class DepositRequestRepository(ABC):
    @abstractmethod
    def add_deposit_request(
        self, person_id: uuid.UUID, amount: float
    ) -> DepositRequest:
        raise NotImplementedError

    @abstractmethod
    def get_queued_deposit_requests(self) -> list[DepositRequest]:
        raise NotImplementedError

    @abstractmethod
    def get_deposit_request(self, deposit_request_id: uuid.UUID) -> DepositRequest:
        raise NotImplementedError

    @abstractmethod
    def update_deposit_request_status(
        self, deposit_request_id: uuid.UUID, new_deposit_request_status: DepositStatus
    ) -> None:
        raise NotImplementedError
