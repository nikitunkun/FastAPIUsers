# pylint: disable=E0401
import pytest
from httpx import codes

from src.tests.conftest import TestClientBase


@pytest.mark.usefixtures("client")
class TestDummy(TestClientBase):
    @staticmethod
    def get_endpoint() -> str:
        return "/dummy"

    @pytest.mark.asyncio
    async def test_success(self) -> None:
        response = await self.client.get(self.get_endpoint())

        assert response.status_code == codes.OK
        assert response.json() == {"data": {"Hello": "World"}}
