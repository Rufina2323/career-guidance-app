from datetime import timedelta
import datetime
from typing import Annotated
import uuid
from create_entites.inference_data.impl.career_prediction_model_inference_data import (
    CareerPredictionModelInferenceDataCreateEntity,
)
from dtos.deposit_request_dto import DepositRequestDTO
from dtos.inference_data_dto import InferenceDataDTO
from dtos.ml_model_dto import MLModelDTO
from dtos.ml_request_dto import MLRequestDTO
from dtos.response_data_dto import ResponseDataDTO
from dtos.token import Token
from dtos.register_person_dto import RegisterPersonDTO, RegisterRole
from dtos.transaction_dto import TransactionDTO
from dtos.person_dto import PersonDTO
from fastapi import FastAPI, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse

from create_entites.person.impl.admin import AdminCreateEntity
from create_entites.person.impl.user import UserCreateEntity
from entities.person.impl.user import User
from models.ml_request import Status
from services.admin_service import AdminService
from services.balance_service import BalanceService
from services.deposit_request_service import DepositRequestService
from services.ml_model_service import MLModelService
from services.ml_request_service import MLRequestService
import uvicorn
import logging

from services.transaction_service import TransactionService
from services.user_service import UserService

from config.rabbitmq import RABBITMQ_QUEUE

from jose import jwt, JWTError
from starlette import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from messaging.rabbitmq import publish

import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

assert SECRET_KEY is not None
assert ALGORITHM is not None


# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Сервисное API", description="API для управления событиями", version="1.0.0"
)

oath2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

ml_request_service = MLRequestService()
balance_service = BalanceService()
user_service = UserService()
admin_service = AdminService()
transaction_service = TransactionService()
ml_model_service = MLModelService()
deposit_request_service = DepositRequestService()


@app.post("/auth", status_code=status.HTTP_201_CREATED)
def register(register_person_dto: RegisterPersonDTO) -> dict[str, str]:
    if register_person_dto.role == RegisterRole.USER:
        success, result = user_service.add_person(
            UserCreateEntity(
                username=register_person_dto.username,
                email=register_person_dto.email,
                password=register_person_dto.password,
            )
        )
    else:
        success, result = admin_service.add_person(
            AdminCreateEntity(
                username=register_person_dto.username,
                email=register_person_dto.email,
                password=register_person_dto.password,
            )
        )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    return {"message": "User created successfully.", "user_id": str(result.user_id)}


@app.post("/auth/token", response_model=Token)
def login_for_access_token(user_login: Annotated[OAuth2PasswordRequestForm, Depends()]):
    person = user_service.authenticate_person(user_login.username, user_login.password)
    if person:
        person_role = user_service.get_person_role(person.user_id)
        expired = datetime.datetime.now(datetime.UTC) + timedelta(minutes=20)
        encode = {
            "sub": person.username,
            "role": person_role,
            "id": str(person.user_id),
            "exp": expired,
        }
        token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password.",
    )


async def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "user_id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/role")
def get_role(user: user_dependency) -> dict[str, str]:
    return {"role": user["role"]}


@app.get("/balance")
def get_balance(user: user_dependency) -> dict[str, float]:
    balance_id = user_service.get_user_balance_id(uuid.UUID(user["user_id"]))
    if not balance_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    balance = balance_service.get_balance(balance_id)
    if not balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Balance does not exist."
        )
    return {"balance": balance.amount}


@app.post("/deposit_request", status_code=status.HTTP_200_OK)
def request_deposit(user: user_dependency, amount: float) -> dict[str, str]:
    person_id = uuid.UUID(user["user_id"])
    person = admin_service.get_person(person_id)
    if not person:
        person = user_service.get_person(person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
    deposit_request = user_service.request_deposit(person_id, amount)
    return {
        "deposit request": str(deposit_request.deposit_id),
        "deposit amount": str(deposit_request.amount),
    }


@app.get("/admin/deposit_requests", status_code=status.HTTP_200_OK)
def get_deposit_requests(user: user_dependency) -> list[DepositRequestDTO]:
    person = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )
    queued_deposit_requests = admin_service.get_queued_deposit_requests()
    return [
        DepositRequestDTO(
            deposit_id=queued_deposit_request.deposit_id,
            amount=queued_deposit_request.amount,
            timestamp=queued_deposit_request.timestamp,
            username=user_service.get_person(queued_deposit_request.person_id).username,
        )
        for queued_deposit_request in queued_deposit_requests
    ]


@app.put("/admin/balance", status_code=status.HTTP_200_OK)
def update_balance(user: user_dependency, deposit_request_id: uuid.UUID) -> None:
    admin = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )
    deposit_request = deposit_request_service.get_deposit_request(deposit_request_id)
    if not user_service.get_person(deposit_request.person_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    try:
        admin_service.deposit_to_user(deposit_request.person_id, deposit_request.amount)
        admin_service.complete_deposit_request(deposit_request_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/admin/balance_deposit_reject", status_code=status.HTTP_200_OK)
def reject_balance_deposit(
    user: user_dependency, deposit_request_id: uuid.UUID
) -> None:
    admin = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )
    deposit_request = deposit_request_service.get_deposit_request(deposit_request_id)
    if not user_service.get_person(deposit_request.person_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    try:
        admin_service.reject_deposit_request(deposit_request_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/admin/all_users", status_code=status.HTTP_200_OK)
def get_all_users(user: user_dependency) -> list[PersonDTO]:
    admin = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )
    users = admin_service.get_all_users()
    users_dto = []
    for user in users:
        user_id = user_service.get_user_id_by_username(user.username)
        users_dto.append(
            PersonDTO(
                username=user.username,
                role=user_service.get_person_role(user_id),
                user_id=user_id,
            )
        )
    return users_dto


@app.get("/admin/transaction_history")
def get_user_transaction_history_for_admin(
    user: user_dependency, user_id: uuid.UUID
) -> list[TransactionDTO]:
    person = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )

    return get_transaction_history(user_id=user_id)


def get_transaction_history(user_id: uuid.UUID) -> list[TransactionDTO]:
    user = user_service.get_person(user_id)
    if not user:
        user = admin_service.get_person(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
            )

    balance_id = user_service.get_user_balance_id(user_id)
    transaction_history = transaction_service.get_transaction_history(balance_id)

    result = []
    for transaction in transaction_history:
        if hasattr(transaction, "ml_request"):
            transaction_type = "ml_request"
        else:
            transaction_type = "deposit"

        result.append(
            TransactionDTO(
                transaction_type=transaction_type,
                amount=transaction.amount,
                timestamp=transaction.timestamp,
            )
        )
    return result


@app.get("/admin/transaction_history")
def get_user_transaction_history_for_admin(
    user: user_dependency, user_id: uuid.UUID
) -> list[TransactionDTO]:
    person = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )

    return get_transaction_history(user_id=user_id)


@app.get("/transaction_history")
def get_user_transaction_history(user: user_dependency) -> list[TransactionDTO]:
    return get_transaction_history(user_id=uuid.UUID(user["user_id"]))


@app.get("/all_ml_models")
def get_all_ml_models(user: user_dependency) -> list[MLModelDTO]:
    ml_models = ml_model_service.get_all_ml_models()
    return [
        MLModelDTO(id=m.model_id, name=m.name, cost=m.request_cost) for m in ml_models
    ]


@app.get("/ml_request_history")
def get_ml_request_history(user: user_dependency) -> list[MLRequestDTO]:
    ml_request_history = ml_request_service.get_ml_request_history(
        uuid.UUID(user["user_id"])
    )

    result = []
    for ml_request in ml_request_history:
        inference_data = InferenceDataDTO(
            operating_systems_percentage=ml_request.inference_data.operating_systems_percentage,
            algorithms_percentage=ml_request.inference_data.algorithms_percentage,
            programming_concepts_percentage=ml_request.inference_data.programming_concepts_percentage,
            computer_networks_percentage=ml_request.inference_data.computer_networks_percentage,
            software_engineering_percentage=ml_request.inference_data.software_engineering_percentage,
            electronics_subjects_percentage=ml_request.inference_data.electronics_subjects_percentage,
            computer_architecture_percentage=ml_request.inference_data.computer_architecture_percentage,
            mathematics_percentage=ml_request.inference_data.mathematics_percentage,
            communication_skills_percentage=ml_request.inference_data.communication_skills_percentage,
            hours_working_per_day=ml_request.inference_data.hours_working_per_day,
            logical_quotient_rating=ml_request.inference_data.logical_quotient_rating,
            hackathons=ml_request.inference_data.hackathons,
            coding_skills_rating=ml_request.inference_data.coding_skills_rating,
            public_speaking_points=ml_request.inference_data.public_speaking_points,
            can_work_long_time=ml_request.inference_data.can_work_long_time,
            self_learning_capability=ml_request.inference_data.self_learning_capability,
            extra_courses_did=ml_request.inference_data.extra_courses_did,
            certifications=ml_request.inference_data.certifications,
            workshops=ml_request.inference_data.workshops,
            talent_tests_taken=ml_request.inference_data.talent_tests_taken,
            olympiads=ml_request.inference_data.olympiads,
            reading_writing_skills=ml_request.inference_data.reading_writing_skills,
            memory_capability_score=ml_request.inference_data.memory_capability_score,
            interested_subjects=ml_request.inference_data.interested_subjects,
            interested_career_area=ml_request.inference_data.interested_career_area,
            job_higher_studies=ml_request.inference_data.job_higher_studies,
            company_type_prefered=ml_request.inference_data.company_type_prefered,
            taken_inputs_from_elders=ml_request.inference_data.taken_inputs_from_elders,
            interested_in_games=ml_request.inference_data.interested_in_games,
            interested_book_types=ml_request.inference_data.interested_book_types,
            salary_range_expected=ml_request.inference_data.salary_range_expected,
            in_realtionship=ml_request.inference_data.in_realtionship,
            behaviour=ml_request.inference_data.behaviour,
            management_or_technical=ml_request.inference_data.management_or_technical,
            worker_type=ml_request.inference_data.worker_type,
            team_work=ml_request.inference_data.team_work,
            introvert=ml_request.inference_data.introvert,
        )

        response_data = ResponseDataDTO(
            job_role_result=ml_request.response_data.job_role_result
        )

        result.append(
            MLRequestDTO(
                ml_model_name=ml_request.ml_model.name,
                ml_model_request_cost=ml_request.ml_model.request_cost,
                inference_data=inference_data,
                response_data=response_data,
                status=ml_request.status,
                timestamp=ml_request.timestamp,
            )
        )
    return result


@app.post("/ml_request")
def create_ml_request(
    user: user_dependency, payload: InferenceDataDTO, ml_model_id: uuid.UUID
):
    user_id = uuid.UUID(user["user_id"])
    balance_id = user_service.get_user_balance_id(user_id)
    if not balance_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Balance does not exist."
        )

    input_data_create_entity = CareerPredictionModelInferenceDataCreateEntity(
        operating_systems_percentage=payload.operating_systems_percentage,
        algorithms_percentage=payload.algorithms_percentage,
        programming_concepts_percentage=payload.programming_concepts_percentage,
        computer_networks_percentage=payload.computer_networks_percentage,
        software_engineering_percentage=payload.software_engineering_percentage,
        electronics_subjects_percentage=payload.electronics_subjects_percentage,
        computer_architecture_percentage=payload.computer_architecture_percentage,
        mathematics_percentage=payload.mathematics_percentage,
        communication_skills_percentage=payload.communication_skills_percentage,
        hours_working_per_day=payload.hours_working_per_day,
        logical_quotient_rating=payload.logical_quotient_rating,
        hackathons=payload.hackathons,
        coding_skills_rating=payload.coding_skills_rating,
        public_speaking_points=payload.public_speaking_points,
        can_work_long_time=payload.can_work_long_time,
        self_learning_capability=payload.self_learning_capability,
        extra_courses_did=payload.extra_courses_did,
        certifications=payload.certifications,
        workshops=payload.workshops,
        talent_tests_taken=payload.talent_tests_taken,
        olympiads=payload.olympiads,
        reading_writing_skills=payload.reading_writing_skills,
        memory_capability_score=payload.memory_capability_score,
        interested_subjects=payload.interested_subjects,
        interested_career_area=payload.interested_career_area,
        job_higher_studies=payload.job_higher_studies,
        company_type_prefered=payload.company_type_prefered,
        taken_inputs_from_elders=payload.taken_inputs_from_elders,
        interested_in_games=payload.interested_in_games,
        interested_book_types=payload.interested_book_types,
        salary_range_expected=payload.salary_range_expected,
        in_realtionship=payload.in_realtionship,
        behaviour=payload.behaviour,
        management_or_technical=payload.management_or_technical,
        worker_type=payload.worker_type,
        team_work=payload.team_work,
        introvert=payload.introvert,
    )

    response_data_id = uuid.uuid4()

    try:
        ml_request_id = ml_request_service.create_ml_request(
            user_id,
            balance_id,
            ml_model_id,
            response_data_id,
            input_data_create_entity,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    publish(
        queue=RABBITMQ_QUEUE,
        message={
            "request_id": str(ml_request_id),
            "ml_model_id": str(ml_model_id),
            "payload": payload.dict(),
            "response_data_id": str(response_data_id),
        },
    )
    return {"request_id": str(ml_request_id), "status": "queued"}


@app.get("/prediction")
def get_prediction(user: user_dependency, ml_request_id: uuid.UUID) -> dict[str, str]:
    user_id = ml_request_service.get_user_id(ml_request_id)
    if user_id != uuid.UUID(user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have access."
        )
    ml_request_status = ml_request_service.get_ml_request_status(ml_request_id)
    if ml_request_status == Status.FAILED:
        raise HTTPException(status_code=404, detail="Prediction failed")

    if ml_request_status == Status.RUNNING or ml_request_status == Status.QUEUED:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    prediction = ml_request_service.get_prediction(ml_request_id)
    return {"prediction": prediction.job_role_result}


@app.get("/", response_model=dict[str, str])
async def index() -> dict[str, str]:
    """
    Корневой эндпоинт, возвращающий приветственное сообщение с информацией о пользователе.

    Returns:
        dict[str, str]: Приветственное сообщение с информацией о пользователе
    """
    try:
        user = User(id=1, email="Nick@gmail.com", password="12345678")
        logger.info(f"Успешное выполнение маршрута index для пользователя: {user}")
        return {"message": f"Hello world! User: {user}"}
    except Exception as e:
        logger.error(f"Ошибка в маршруте index: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Эндпоинт проверки работоспособности для мониторинга.

    Returns:
        dict[str, str]: Сообщение о статусе
    """
    logger.info("Эндпоинт health_check успешно вызван")
    return {"status": "healthy"}


# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTPException: {exc.detail} для запроса {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="debug")
