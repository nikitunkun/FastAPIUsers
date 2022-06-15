# pylint: disable=E0401
import uuid

import pytest
from httpx import codes
from requests.auth import HTTPBasicAuth

from src.tests.conftest import TestClientBase


@pytest.mark.usefixtures("client")
class TestUser(TestClientBase):
    @staticmethod
    def get_endpoint(path: str) -> str:
        return f"/user{path}"

    @pytest.mark.asyncio
    async def test_success(self) -> None:
        id_ = str(uuid.uuid4())
        username = "test"
        password = "test"
        auth = HTTPBasicAuth(username=username, password=password)

        # Test User Create
        response = await self.client.post(
            self.get_endpoint("/create"), json={"id": id_, "username": username, "password": password}
        )
        assert response.status_code == codes.OK

        # Test User Get
        response = await self.client.get(self.get_endpoint("/"), auth=auth)
        assert response.status_code == codes.OK
        assert response.json()["id"] == id_

        # Test User Update
        response = await self.client.put(
            self.get_endpoint("/"), auth=auth, json={"username": username * 2, "password": password}
        )
        assert response.status_code == codes.OK
        assert response.json()["username"] == username * 2
