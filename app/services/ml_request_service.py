import uuid
from create_entites.inference_data.inference_data import InferenceDataCreateEntity
from entities.ml_request import MLRequest
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from entities.response_data.response_data import ResponseData
from models.ml_request import Status
from repositories.ml_request.impl.ml_request_psql_repository import (
    MLRequestPSQLRepository,
)
from repositories.ml_request.repository import MLRequestRepository
from services.balance_service import BalanceService
from services.inference_data_service import InferenceDataService
from services.ml_model_service import MLModelService
from services.response_data_service import ResponseDataService
from services.user_service import UserService


class MLRequestService:
    def __init__(self) -> None:
        self.balance_service = BalanceService()
        self.user_service = UserService()
        self.ml_model_service = MLModelService()
        self.inference_data_service = InferenceDataService()
        self.response_data_service = ResponseDataService()
        self.ml_request_repository: MLRequestRepository = MLRequestPSQLRepository()

    def create_ml_request(
        self,
        user_id: uuid.UUID,
        balance_id: uuid.UUID,
        model_id: uuid.UUID,
        repsonse_data_id: uuid.UUID,
        inference_data: InferenceDataCreateEntity,
    ) -> uuid.UUID:
        model_cost = self.ml_model_service.get_ml_model_request_cost(model_id)
        self.balance_service.can_withdraw(balance_id, model_cost)

        inference_data_id = self.inference_data_service.add_data(inference_data)
        self.response_data_service.add_data(
            repsonse_data_id, CareerPredictionModelResponseData(job_role_result="")
        )

        ml_request_id = self.ml_request_repository.create_ml_request(
            model_cost, user_id, model_id, inference_data_id, repsonse_data_id
        )

        self.balance_service.withdraw(ml_request_id, balance_id, model_cost)
        return ml_request_id
    
    def fail_ml_request(self, ml_request_id: uuid.UUID) -> None:
        user_id = self.ml_request_repository.get_user_id(ml_request_id)
        balance_id = self.user_service.get_user_balance_id(user_id)
        model_cost = self.ml_request_repository.get_ml_request_cost(ml_request_id)
        self.balance_service.deposit(balance_id, model_cost)


    def change_ml_request_status(self, ml_request_id: uuid.UUID, ml_request_status: Status) -> None:
        self.ml_request_repository.change_ml_request_status(ml_request_id, ml_request_status)

    def get_user_id(self, ml_request_id: uuid.UUID) -> uuid.UUID:
        return self.ml_request_repository.get_user_id(ml_request_id)
    
    def get_ml_request_status(self, ml_request_id: uuid.UUID) -> Status:
        return self.ml_request_repository.get_ml_request_status(ml_request_id)

    def get_prediction(self, ml_request_id: uuid.UUID) -> ResponseData:
        response_data_id = self.ml_request_repository.get_prediction_id(ml_request_id)
        return self.response_data_service.get_data(response_data_id)

    def get_ml_request_history(self, user_id: uuid.UUID) -> list[MLRequest]:
        ml_requests = self.ml_request_repository.get_ml_request_history(user_id)

        ml_requests.sort(key=lambda ml_request: ml_request.timestamp, reverse=True)

        return ml_requests
