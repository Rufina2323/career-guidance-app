import datetime
import uuid
from entities.deposit_request import DepositRequest
from models.person import Person as PersonModel
from models.deposit_request import DepositStatus
from repositories.deposit_request.repository import DepositRequestRepository
from sqlmodel import Session, select
from database.engine import engine
from models.deposit_request import DepositRequest as DepositRequestModel


class DepositRequestPSQLRepository(DepositRequestRepository):
    def __init__(self):
        self.session_maker = Session

    def add_deposit_request(
        self, person_id: uuid.UUID, amount: float
    ) -> DepositRequest:
        with self.session_maker(engine) as session:
            statement = select(PersonModel).where(PersonModel.id == person_id)
            psql_person = session.exec(statement).first()

            deposit_request_model = DepositRequestModel(
                amount=amount,
                deposit_status=DepositStatus.QUEUED,
                timestamp=datetime.datetime.now(),
                person=psql_person,
            )
            session.add(deposit_request_model)
            session.commit()

            return DepositRequest(
                deposit_id=deposit_request_model.id,
                amount=deposit_request_model.amount,
                deposit_status=deposit_request_model.deposit_status,
                timestamp=deposit_request_model.timestamp,
                person_id=person_id,
            )

    def get_queued_deposit_requests(self) -> list[DepositRequest]:
        with self.session_maker(engine) as session:
            statement = select(DepositRequestModel).where(
                DepositRequestModel.deposit_status == DepositStatus.QUEUED
            )
            psql_queued_deposit_requests = session.exec(statement).all()

            queued_deposit_requests = []

            for queued_deposit_request in psql_queued_deposit_requests:
                queued_deposit_requests.append(
                    DepositRequest(
                        deposit_id=queued_deposit_request.id,
                        amount=queued_deposit_request.amount,
                        deposit_status=queued_deposit_request.deposit_status,
                        timestamp=queued_deposit_request.timestamp,
                        person_id=queued_deposit_request.person_id,
                    )
                )

            return queued_deposit_requests

    def get_deposit_request(self, deposit_request_id: uuid.UUID) -> DepositRequest:
        with self.session_maker(engine) as session:
            statement = select(DepositRequestModel).where(
                DepositRequestModel.id == deposit_request_id
            )
            psql_deposit_request = session.exec(statement).first()
            return DepositRequest(
                deposit_id=psql_deposit_request.id,
                amount=psql_deposit_request.amount,
                deposit_status=psql_deposit_request.deposit_status,
                timestamp=psql_deposit_request.timestamp,
                person_id=psql_deposit_request.person_id,
            )

    def update_deposit_request_status(
        self, deposit_request_id: uuid.UUID, new_deposit_request_status: DepositStatus
    ) -> None:
        with self.session_maker(engine) as session:
            statement = select(DepositRequestModel).where(
                DepositRequestModel.id == deposit_request_id
            )
            psql_deposit_request = session.exec(statement).first()
            psql_deposit_request.deposit_status = new_deposit_request_status
            session.commit()
