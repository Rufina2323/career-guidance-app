import uuid
from entities.deposit_request import DepositRequest
from models.deposit_request import DepositStatus
from repositories.deposit_request.impl.deposit_request_psql_repository import (
    DepositRequestPSQLRepository,
)
from repositories.deposit_request.repository import DepositRequestRepository


class DepositRequestService:
    def __init__(self) -> None:
        self.deposit_request_repository: DepositRequestRepository = (
            DepositRequestPSQLRepository()
        )

    def add_deposit_request(
        self, person_id: uuid.UUID, amount: float
    ) -> DepositRequest:
        return self.deposit_request_repository.add_deposit_request(person_id, amount)

    def get_queued_deposit_requests(self) -> list[DepositRequest]:
        return self.deposit_request_repository.get_queued_deposit_requests()

    def get_deposit_request(self, deposit_request_id: uuid.UUID) -> DepositRequest:
        return self.deposit_request_repository.get_deposit_request(deposit_request_id)

    def update_deposit_request_status(
        self, deposit_request_id: uuid.UUID, new_deposit_request_status: DepositStatus
    ) -> None:
        return self.deposit_request_repository.update_deposit_request_status(
            deposit_request_id, new_deposit_request_status
        )
