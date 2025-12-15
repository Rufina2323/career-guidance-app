from datetime import timedelta
import datetime
from typing import Annotated
import uuid
from create_entites.inference_data.impl.career_prediction_model_inference_data import (
    CareerPredictionModelInferenceDataCreateEntity,
)
from dtos.inference_data_dto import InferenceDataDTO
from dtos.update_balance_dto import UpdateBalanceDTO
from dtos.token import Token
from dtos.register_person_dto import RegisterPersonDTO, RegisterRole
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse

from create_entites.person.impl.admin import AdminCreateEntity
from create_entites.person.impl.user import UserCreateEntity
from entities.person.impl.user import User
from services.admin_service import AdminService
from services.balance_service import BalanceService
from services.ml_request_service import MLRequestService
import uvicorn
import logging

from services.transaction_service import TransactionService
from services.user_service import UserService

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
        expired = datetime.datetime.now(datetime.UTC) + timedelta(minutes=20)
        encode = {"sub": person.username, "id": str(person.user_id), "exp": expired}
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
        print(username, user_id)
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]


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


@app.put("/admin/balance", status_code=status.HTTP_200_OK)
def update_balance(
    user: user_dependency, user_id: uuid.UUID, update_balance_dto: UpdateBalanceDTO
) -> None:
    person = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )
    if not user_service.get_person(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    try:
        admin_service.deposit_to_user(user_id, update_balance_dto.amount)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_transaction_history(user_id: uuid.UUID) -> list[str]:
    user = user_service.get_person(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist."
        )

    balance_id = user_service.get_user_balance_id(user_id)
    transaction_history = transaction_service.get_transaction_history(balance_id)

    result = []
    for transaction in transaction_history:
        transaction_string = (
            "transaction.amount"
            + str(transaction.amount)
            + "transaction.timestamp"
            + str(transaction.timestamp)
        )
        if hasattr(transaction, "ml_request"):
            transaction_string = "ml_request, " + transaction_string
        else:
            transaction_string = "deposit, " + transaction_string
        result.append(transaction_string)
    return result


@app.get("/admin/transaction_history")
def get_user_transaction_history_for_admin(
    user: user_dependency, user_id: uuid.UUID
) -> list[str]:
    person = admin_service.get_person(uuid.UUID(user["user_id"]))
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin."
        )

    return get_transaction_history(user_id=user_id)


@app.get("/transaction_history")
def get_user_transaction_history(user: user_dependency) -> list[str]:
    return get_transaction_history(user_id=uuid.UUID(user["user_id"]))


@app.get("/ml_request_history")
def get_ml_request_history(user: user_dependency) -> list[str]:
    ml_request_history = ml_request_service.get_ml_request_history(
        uuid.UUID(user["user_id"])
    )

    result = []
    for ml_request in ml_request_history:
        ml_request_string = (
            "ml_request.timestamp"
            + str(ml_request.timestamp)
            + "ml_request.person.username"
            + str(ml_request.person.username)
            + "ml_request.response_data"
            + str(ml_request.response_data)
        )

        result.append(ml_request_string)
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
        instrovert=payload.instrovert,
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
        queue="ml_requests",
        message={
            "request_id": str(ml_request_id),
            "ml_model_id": str(ml_model_id),
            "payload": payload.dict(),
            "response_data_id": str(response_data_id),
        },
    )
    return {"request_id": str(ml_request_id), "status": "queued"}


@app.get("/prediction")
def get_prediction(user: user_dependency, ml_request_id: uuid.UUID) -> None:
    user_id = ml_request_service.get_user_id(ml_request_id)
    if user_id != uuid.UUID(user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have access."
        )
    prediction = ml_request_service.get_prediction(ml_request_id)
    if prediction.job_role_result == "":
        raise HTTPException(status_code=404, detail="Prediction not ready or not found")

    ml_request_service.finish_ml_request(ml_request_id=ml_request_id)
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
