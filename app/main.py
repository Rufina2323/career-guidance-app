import uuid
from dtos.update_balance_dto import UpdateBalanceDTO
from dtos.user_login_dto import UserLoginDTO
from dtos.register_person_dto import RegisterPersonDTO, RegisterRole
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse

from authx import AuthX, AuthXConfig

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

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Сервисное API", description="API для управления событиями", version="1.0.0"
)

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = "SECRETE_KEY"
auth_config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=auth_config)

ml_request_service = MLRequestService()
balace_service = BalanceService()
user_service = UserService()
admin_service = AdminService()
transaction_service = TransactionService()


@app.post("/login")
def login(user_login_dto: UserLoginDTO, response: Response):
    person = user_service.authenticate_person(user_login_dto.username, user_login_dto.password)
    if person:
        token = security.create_access_token(uid=str(person.user_id))
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/protected")
def protected(login_user = Depends(security.access_token_required)):
    return login_user


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


@app.post("/register")
def register(register_person_dto: RegisterPersonDTO) -> dict[str, str]:
    if register_person_dto.role == RegisterRole.USER:
        success, result = user_service.add_person(
            UserCreateEntity(
                username=register_person_dto.username,
                email=register_person_dto.email,
                password=register_person_dto.password
            )
        )
    else:
        success, result = admin_service.add_person(
            AdminCreateEntity(
                username=register_person_dto.username,
                email=register_person_dto.email,
                password=register_person_dto.password
            )
        )
    if not success:
        raise HTTPException(status_code=400, detail=result)
    return {"message": "Admin created successfully", "user_id": str(result.user_id)}
    

@app.get("/balance")
def get_balance(user_id: uuid.UUID) -> dict[str, float]:
    balance = user_service.get_balance(user_id)
    if not balance:
            raise HTTPException(status_code=400, detail="user_id does not exists")
    return {"balance": balance.amount}
    
    
@app.put("/balance")
def update_balance(user_id: uuid.UUID, update_balance_dto: UpdateBalanceDTO) -> None:
    user = user_service.get_person(user_id)
    admin_service.deposit_to_user(user, update_balance_dto.amount)


# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTPException: {exc.detail} для запроса {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="debug")
