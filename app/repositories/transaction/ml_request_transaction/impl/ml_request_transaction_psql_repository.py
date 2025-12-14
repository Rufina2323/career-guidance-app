import datetime
from entities.balance import Balance
from entities.ml_model.impl.career_prediction_model import CareerPredictionModel
from entities.ml_request import MLRequest
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from entities.transaction.impl.ml_request_transaction import MLRequestTransaction
from models.ml_request_transaction import (
    MLRequestTransaction as MLRequestTransactionModel,
)
from models.person import Person as PersonModel
from models.inference_data import InferenceData as InferenceDataModel

import uuid

from sqlmodel import Session, select
from database.engine import engine
from repositories.transaction.impl.transaction_psql_repository import (
    TransactionPSQLRepository,
)
from repositories.transaction.ml_request_transaction.ml_request_transaction_repository import (
    MLRequestTransactionRepository,
)


class MLRequestTransactionPSQLRepository(
    MLRequestTransactionRepository, TransactionPSQLRepository
):
    def create_transaction(
        self, ml_request_id: uuid.UUID, balance_id: uuid.UUID, amount: float
    ) -> None:
        ml_request_transaction_model = MLRequestTransactionModel(
            amount=amount,
            timestamp=datetime.datetime.now(),
            ml_request_id=ml_request_id,
            balance_id=balance_id,
        )

        with Session(engine) as session:
            session.add(ml_request_transaction_model)
            session.commit()

    def get_all_transactions(self, balance_id: uuid.UUID) -> list[MLRequestTransaction]:
        statement = select(MLRequestTransactionModel).where(
            MLRequestTransactionModel.balance_id == balance_id
        )
        with Session(engine) as session:
            psql_ml_request_transactions = session.exec(statement).all()
            ml_request_transactions = []
            for tx in psql_ml_request_transactions:
                person = PersonModel.to_domain(tx.ml_request.person)
                ml_model = CareerPredictionModel(
                    model_id=tx.ml_request.ml_model.id,
                    name=tx.ml_request.ml_model.name,
                    request_cost=tx.ml_request.ml_model.request_cost,
                    model_path=tx.ml_request.ml_model.model_path,
                    preprocessing_path=tx.ml_request.ml_model.preprocessing_path,
                )
                inference_data = InferenceDataModel.to_domain(
                    tx.ml_request.inference_data
                )
                response_data = CareerPredictionModelResponseData(
                    job_role_result=tx.ml_request.response_data
                )

                ml_request_transactions.append(
                    MLRequestTransaction(
                        balance=Balance(
                            amount=tx.balance.amount,
                        ),
                        amount=tx.amount,
                        timestamp=tx.timestamp,
                        ml_request=MLRequest(
                            person=person,
                            ml_model=ml_model,
                            inference_data=inference_data,
                            response_data=response_data,
                            status=tx.ml_request.status,
                            timestamp=tx.ml_request.timestamp,
                        ),
                    )
                )

        return ml_request_transactions
