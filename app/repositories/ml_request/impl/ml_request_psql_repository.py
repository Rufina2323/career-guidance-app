import datetime
import uuid
from sqlmodel import Session, select
from database.engine import engine
from entities.ml_request import MLRequest
from models.ml_request import MLRequest as MLRequestModel

from repositories.ml_request.repository import MLRequestRepository

from entities.ml_model.impl.career_prediction_model import CareerPredictionModel
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from models.person import Person as PersonModel
from models.inference_data import InferenceData as InferenceDataModel


class MLRequestPSQLRepository(MLRequestRepository):
    def create_ml_request(
        self,
        model_cost: float,
        user_id: uuid.UUID,
        model_id: uuid.UUID,
        inference_data_id: uuid.UUID,
        repsonse_data_id: uuid.UUID,
    ) -> uuid.UUID:
        ml_request_model = MLRequestModel(
            status="queued",
            timestamp=datetime.datetime.now(),
            credits_used=model_cost,
            user_id=user_id,
            ml_model_id=model_id,
            inference_data_id=inference_data_id,
            response_data_id=repsonse_data_id,
        )

        with Session(engine) as session:
            session.add(ml_request_model)
            session.commit()
            return ml_request_model.id

    def finish_ml_request(self, ml_request_id: uuid.UUID) -> None:
        with Session(engine) as session:
            statement = select(MLRequestModel).where(MLRequestModel.id == ml_request_id)
            psql_ml_request = session.exec(statement).first()
            psql_ml_request.status = "finished"
            psql_ml_request.timestamp = datetime.datetime.now()
            session.commit()

    def get_prediction_id(self, ml_request_id: uuid.UUID) -> uuid.UUID:
        with Session(engine) as session:
            statement = select(MLRequestModel).where(MLRequestModel.id == ml_request_id)
            psql_ml_request = session.exec(statement).first()
            return psql_ml_request.response_data_id

    def get_user_id(self, ml_request_id: uuid.UUID) -> uuid.UUID:
        with Session(engine) as session:
            statement = select(MLRequestModel).where(MLRequestModel.id == ml_request_id)
            psql_ml_request = session.exec(statement).first()
            return psql_ml_request.user_id

    def get_ml_request_history(self, user_id: uuid.UUID) -> list[MLRequest]:
        with Session(engine) as session:
            statement = select(MLRequestModel).where(MLRequestModel.user_id == user_id)
            psql_ml_requests = session.exec(statement).all()
            ml_requests = []
            for ml_request in psql_ml_requests:
                person = PersonModel.to_domain(ml_request.person)
                ml_model = CareerPredictionModel(
                    model_id=ml_request.ml_model.id,
                    name=ml_request.ml_model.name,
                    request_cost=ml_request.ml_model.request_cost,
                    model_path=ml_request.ml_model.model_path,
                    preprocessing_path=ml_request.ml_model.preprocessing_path,
                    label_encoder_path=ml_request.ml_model.label_encoder_path,
                )
                inference_data = InferenceDataModel.to_domain(ml_request.inference_data)
                response_data = CareerPredictionModelResponseData(
                    job_role_result=ml_request.response_data
                )
                ml_requests.append(
                    MLRequest(
                        person=person,
                        ml_model=ml_model,
                        inference_data=inference_data,
                        response_data=response_data,
                        status=ml_request.status,
                        timestamp=ml_request.timestamp,
                    )
                )
        return ml_requests
