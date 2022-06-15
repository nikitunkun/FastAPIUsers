from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.apps.base.exceptions import setup_exception_handlers
from src.apps.base.integrations.db import DBClient
from src.apps.base.routes import setup_routes


def bootstrap(app: FastAPI) -> None:
    @app.on_event("shutdown")
    async def shutdown() -> None:  # pylint: disable=W0612
        await DBClient.close()


def build_app() -> FastAPI:

    app = FastAPI()

    bootstrap(app)
    setup_exception_handlers(app)
    setup_routes(app)

    Instrumentator().instrument(app).expose(app)

    return app
