from entities.inference_data.inference_data import InferenceData
from entities.ml_model.ml_model import MLModel
from entities.ml_request import MLRequest
from entities.person.impl.user import User
from services.balance_service import BalanceService


class MLRequestService:
    def __init__(self) -> None:
        self.balance_service = BalanceService()

    def create_ml_request(
        self, user: User, model: MLModel, input_data: InferenceData
    ) -> MLRequest:
        pass

    def get_ml_request_history(self, user: User) -> list[MLRequest]:
        pass
