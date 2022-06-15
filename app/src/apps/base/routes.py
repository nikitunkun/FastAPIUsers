from fastapi import FastAPI

from src.apps.base.transport.handlers import dummy
from src.apps.user.transport.handlers import user


def setup_routes(app: FastAPI) -> None:
    app.include_router(dummy.router, prefix="/dummy", tags=["Тест"])
    app.include_router(user.router, prefix="/user", tags=["Пользователи"])
