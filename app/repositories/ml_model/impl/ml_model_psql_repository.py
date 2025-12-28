import uuid
from entities.ml_model.impl.career_prediction_model import CareerPredictionModel
from entities.ml_model.ml_model import MLModel

from repositories.ml_model.repository import MLModelRepository
from sqlmodel import Session, select
from database.engine import engine
from models.ml_model import MLModel as MLModelModel
from sqlalchemy.exc import NoResultFound


class MLModelPSQLRepository(MLModelRepository):
    def __init__(self):
        self.session_maker = Session

    def get_all_ml_models(self) -> list[MLModel]:
        with self.session_maker(engine) as session:
            statement = select(MLModelModel)
            psql_ml_models = session.exec(statement).all()
            ml_models = []
            for psql_ml_model in psql_ml_models:
                ml_models.append(
                    CareerPredictionModel(
                        model_id=psql_ml_model.id,
                        name=psql_ml_model.name,
                        request_cost=psql_ml_model.request_cost,
                        model_path=psql_ml_model.model_path,
                        preprocessing_path=psql_ml_model.preprocessing_path,
                        label_encoder_path=psql_ml_model.label_encoder_path,
                    )
                )
            return ml_models

    def get_ml_model_request_cost(self, ml_model_id: uuid.UUID) -> float | None:
        with self.session_maker(engine) as session:
            try:
                statement = select(MLModelModel).where(MLModelModel.id == ml_model_id)
                psql_ml_model = session.exec(statement).one()
                return psql_ml_model.request_cost

            except NoResultFound:
                return None

    def get_ml_model(self, ml_model_id: uuid.UUID) -> MLModel:
        with self.session_maker(engine) as session:
            try:
                statement = select(MLModelModel).where(MLModelModel.id == ml_model_id)
                psql_ml_model = session.exec(statement).one()
                return CareerPredictionModel(
                    model_id=psql_ml_model.id,
                    name=psql_ml_model.name,
                    request_cost=psql_ml_model.request_cost,
                    model_path=psql_ml_model.model_path,
                    preprocessing_path=psql_ml_model.preprocessing_path,
                    label_encoder_path=psql_ml_model.label_encoder_path,
                )

            except NoResultFound:
                return None
