import uuid
from entities.response_data.response_data import ResponseData
from repositories.response_data.impl.response_data_psql_repository import (
    ResponseDataPSQLRepository,
)
from repositories.response_data.repository import ResponseDataRepository


class ResponseDataService:
    def __init__(self) -> None:
        self.response_data_repository: ResponseDataRepository = (
            ResponseDataPSQLRepository()
        )

    def add_data(self, response_data: ResponseData) -> uuid.UUID:
        return self.response_data_repository.add_data(response_data)

    def get_data(self, response_data_id: uuid.UUID) -> ResponseData:
        return self.response_data_repository.get_data(response_data_id)
