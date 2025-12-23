import uuid
from entities.response_data.impl.career_prediction_model_response_data import (
    CareerPredictionModelResponseData,
)
from entities.response_data.response_data import ResponseData
from repositories.response_data.repository import ResponseDataRepository
from sqlmodel import Session, select
from database.engine import engine

from sqlalchemy.exc import NoResultFound
from models.response_data import ResponseData as ResponseDataModel


class ResponseDataPSQLRepository(ResponseDataRepository):
    def __init__(self):
        self.session_maker = Session

    def add_data(
        self,
        response_data_id: uuid.UUID,
        response_data: CareerPredictionModelResponseData,
    ) -> uuid.UUID:
        with self.session_maker(engine) as session:
            statement = select(ResponseDataModel).where(
                ResponseDataModel.id == response_data_id
            )
            existing = session.exec(statement).first()

            if existing:
                # Update existing row
                existing.job_role_result = response_data.job_role_result
            else:
                # Insert new row
                existing = ResponseDataModel(
                    id=response_data_id, job_role_result=response_data.job_role_result
                )
                session.add(existing)

            session.commit()
            return existing.id

    def get_data(self, response_data_id: uuid.UUID) -> ResponseData | None:
        with self.session_maker(engine) as session:
            try:
                statement = select(ResponseDataModel).where(
                    ResponseDataModel.id == response_data_id
                )
                psql_response_data = session.exec(statement).one()
                return CareerPredictionModelResponseData(
                    job_role_result=psql_response_data.job_role_result
                )

            except NoResultFound:
                return None
