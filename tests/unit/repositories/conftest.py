from repositories.balance.impl.balance_psql_repository import BalancePSQLRepository

import pytest
from repositories.inference_data.impl.inference_data_psql_repository import InferenceDataPSQLRepository
from repositories.ml_model.impl.ml_model_psql_repository import MLModelPSQLRepository


@pytest.fixture
def balance_psql_repository() -> BalancePSQLRepository:
    return BalancePSQLRepository()


@pytest.fixture
def inference_data_psql_repository():
    return InferenceDataPSQLRepository()

@pytest.fixture
def ml_model_psql_repository():
    return MLModelPSQLRepository()
