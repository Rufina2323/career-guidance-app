from unittest.mock import MagicMock
import pytest

from services.admin_service import AdminService
from services.balance_service import BalanceService
from services.inference_data_service import InferenceDataService
from services.ml_model_service import MLModelService
from services.ml_request_service import MLRequestService
from services.response_data_service import ResponseDataService
from services.transaction_service import TransactionService
from services.user_service import UserService


@pytest.fixture
def admin_service():
    return AdminService()


@pytest.fixture
def balance_service():
    return BalanceService()


@pytest.fixture
def inference_data_service():
    return InferenceDataService()


@pytest.fixture
def response_data_service():
    return ResponseDataService()


@pytest.fixture
def ml_model_service():
    return MLModelService()


@pytest.fixture
def ml_request_service():
    return MLRequestService()


@pytest.fixture
def transaction_service():
    return TransactionService()


@pytest.fixture
def user_service():
    service = UserService()
    service.person_repository = MagicMock()
    return service
