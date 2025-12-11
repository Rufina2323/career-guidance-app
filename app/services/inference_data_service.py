import uuid
from create_entites.inference_data.inference_data import InferenceDataCreateEntity
from entities.inference_data.inference_data import InferenceData
from repositories.inference_data.impl.inference_data_psql_repository import (
    InferenceDataPSQLRepository,
)
from repositories.inference_data.repository import InferenceDataRepository


class InferenceDataService:
    def __init__(self) -> None:
        self.inference_data_repository: InferenceDataRepository = (
            InferenceDataPSQLRepository()
        )

    def add_data(self, inference_data: InferenceDataCreateEntity) -> uuid.UUID:
        return self.inference_data_repository.add_data(inference_data)

    def get_data(self, inference_data_id: uuid.UUID) -> InferenceData:
        return self.inference_data_repository.get_data(inference_data_id)
