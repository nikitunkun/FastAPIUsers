import json
from datetime import timedelta
from typing import Dict, Mapping
from uuid import UUID

from databases.core import Connection
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials

from src.apps.base.di import get_connection
from src.apps.base.exceptions import AuthMismatch
from src.apps.base.integrations.redis import redis
from src.apps.user.repositories.user_repository import UserRepository
from src.apps.user.schemas.requests import UserCreateRequest, UserSearchRequest, UserUpdateRequest
from src.apps.user.schemas.responses import UserGetResponse


class UserService:
    """
    Сервис для приложения User.
    """

    def __init__(self, connection: Connection = Depends(get_connection)) -> None:
        """
        Инициализация сервиса.
        Сервисы используют репозитории для работы с данными.

        :param connection: Объект соединения с БД.
        """

        self.user_repository = UserRepository(connection)

    async def verify(self, credentials: HTTPBasicCredentials) -> Mapping:
        """
        Сервис для проверки авторизции пользователей.

        :param query_params:
        :return:
        """

        result = await self.user_repository.find_one_by(username=credentials.username, password=credentials.password)
        if not result:
            raise AuthMismatch

        return result

    async def find_user(self, query_params: UserSearchRequest) -> Mapping:
        """
        Сервис для метода поиска пользователей.

        :param query_params:
        :return:
        """

        result = await self.user_repository.find_user(search_string=query_params.search_string)
        return result

    async def get_user(self, user_id: UUID) -> Mapping:
        """
        Сервис для метода получения пользователя.

        :param user_id:
        :param query_params:
        :return:
        """

        user_id = str(user_id)
        if await redis.client.exists(user_id):
            return await json.loads(redis.client.get(user_id))

        result = await self.user_repository.find(primary_key=user_id)

        if result:
            await redis.client.setex(
                name=user_id,
                value=UserGetResponse.parse_obj(result).json(),
                time=timedelta(minutes=1),
            )

        return result

    async def create_user(self, request_body: UserCreateRequest) -> UserCreateRequest:
        """
        Сервис для метода создания пользователя.

        :param request_body:
        :return:
        """

        await self.user_repository.create_model(model=request_body)
        return request_body

    async def update_user(self, user_id: UUID, request_body: UserUpdateRequest) -> Dict:
        """
        Сервис для метода обновления пользователя.

        :param user_id:
        :param request_body:
        :return:
        """
        await self.user_repository.update_model(
            primary_key=user_id,
            username=request_body.username,
            password=request_body.password,
        )
        await redis.client.delete(str(user_id))
        return {"id": user_id, **request_body.dict()}

    async def delete_user(self, user_id: UUID) -> Dict:
        """
        Сервис для метода удаления пользователя.

        :param user_id:
        :return:
        """

        await self.user_repository.delete(primary_key=user_id)
        await redis.client.delete(str(user_id))
        return {"id": user_id, "status": "deleted"}
