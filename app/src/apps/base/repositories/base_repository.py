from abc import ABC, abstractmethod
from typing import Any, Dict, Mapping, Optional, Union
from uuid import UUID

from databases.core import Connection
from pydantic.main import BaseModel
from sqlalchemy import Column
from sqlalchemy.sql import FromClause


class BaseRepository(ABC):
    """
    Базовый абстрактный класс репозитория.
    """

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    @property
    @abstractmethod
    def model(self) -> FromClause:
        pass

    def get_attr(self, attr: str) -> Column:
        """
        Получение атрибута модели по наименованию.

        :param attr:
        :return:
        """

        return getattr(self.model.columns, attr)

    async def find(self, primary_key: Union[str, UUID]) -> Optional[Mapping]:
        """
        Поиск объекта по ID.

        :param primary_key:
        :return:
        """

        return await self.connection.fetch_one(query=self.model.select().where(self.get_attr("id") == primary_key))

    async def find_one_by(self, **kwargs: Any) -> Optional[Mapping]:
        """
        Поиск одного объекта по заданным фильтрам.

        :param kwargs:
        :return:
        """

        condition = None
        for attr, value in kwargs.items():
            expression = self.get_attr(attr) == value
            if condition is not None:
                condition &= expression
            else:
                condition = expression

        return await self.connection.fetch_one(query=self.model.select().where(condition))

    async def create_model(self, model: Union[Dict, BaseModel]) -> None:
        """
        Создание записи.

        :param model:
        :return:
        """

        values = model if isinstance(model, dict) else model.dict()
        return await self.connection.execute(self.model.insert(None).values(**values))

    async def update_model(self, primary_key: Union[str, UUID], **kwargs: Any) -> None:
        """
        Обновление записи.

        :param primary_key: Первичный ключ
        :param kwargs: Атрибуты и их значения
        :return:
        """

        statement = self.model.update().where(self.get_attr("id") == primary_key).values(**kwargs)
        await self.connection.execute(statement)

    async def delete_model_by(self, **kwargs: Any) -> None:
        """
        Удаление записи по переданному условию.

        :param kwargs: Значения атрибутов
        :return:
        """

        condition = None
        for attr, value in kwargs.items():
            expression = self.get_attr(attr) == value
            if condition is not None:
                condition &= expression
            else:
                condition = expression

        if condition is not None:
            statement = self.model.delete().where(condition)
            await self.connection.execute(statement)

    async def delete(self, primary_key: Union[str, UUID]) -> None:
        """
        Удаление записи по ID.

        :param primary_key:
        :return:
        """

        await self.connection.execute(self.model.delete().where(self.get_attr("id") == primary_key))
