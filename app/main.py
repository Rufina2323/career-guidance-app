from fastapi import FastAPI, HTTPException, Request
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

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Сервисное API", description="API для управления событиями", version="1.0.0"
)

ml_request_service = MLRequestService()
balace_service = BalanceService()
user_service = UserService()
admin_service = AdminService()
transaction_service = TransactionService()


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


@app.post("/demo")
def demo() -> None:
    user_create_entity = UserCreateEntity(
        username="Anton", email="example123@gmail.com", password="hard_password"
    )
    user = user_service.add_person(user_create_entity)

    admin_create_entity = AdminCreateEntity(
        username="Galina", email="blanka@gmail.com", password="tasty_soup"
    )
    admin_service.add_person(admin_create_entity)

    admin_service.deposit_to_user(user, 600)

    user = user_service.get_person(user.user_id)

    assert user.balance.amount == 600


# Обработчики ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTPException: {exc.detail} для запроса {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="debug")
