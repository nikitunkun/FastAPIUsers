import uuid
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class UserSearchRequest(BaseModel):
    search_string: str = Query(None, title="Значение для поиска")


class UserGetRequest(BaseModel):
    id: Optional[uuid.UUID] = Query(None, title="ID пользователя")


class UserCreateRequest(BaseModel):
    id: uuid.UUID = Field(uuid.uuid4(), title="ID пользователя")
    username: str = Field(..., title="Имя пользователя")
    password: str = Field(..., title="Пароль пользователя")


class UserUpdateRequest(BaseModel):
    username: str = Field(..., title="Имя пользователя")
    password: str = Field(..., title="Пароль пользователя")
