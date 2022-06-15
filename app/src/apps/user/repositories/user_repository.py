from typing import List

from sqlalchemy import Table
from sqlalchemy.sql import select

from src.apps.base.repositories.base_repository import BaseRepository
from src.apps.user.models.user import User


class UserRepository(BaseRepository):
    """
    Класс репозитория для приложения User.
    """

    @property
    def model(self) -> Table:
        return User

    async def find_user(self, search_string: str) -> List:
        """
        Поиск пользоватлей

        :param search_string:
        :return:
        """

        query = select([self.model]).where(self.model.c.username.contains(search_string))
        result = await self.connection.fetch_all(query)
        return result
