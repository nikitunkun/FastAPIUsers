# pylint: disable=E0401, W0621, W0201
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from src.apps.base.integrations.db import DBClient
from src.main import app


@pytest.fixture(scope="function")
async def database() -> AsyncGenerator:
    connection = await DBClient.get_db(force_rollback=True)
    await connection.connect()
    yield
    await connection.disconnect()


@pytest.fixture(scope="function")
async def client(database):
    app.dependency_overrides[DBClient.get_db] = lambda: database
    async with AsyncClient(app=app, base_url="http://localhost") as async_client:
        yield async_client


@pytest.mark.usefixtures("client")
class TestClientBase:
    @pytest.fixture(autouse=True)
    def get_client(self, client: AsyncClient) -> None:
        self.client = client
