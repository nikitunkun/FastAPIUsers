from uuid import UUID

from pydantic import BaseModel, Field


class UserGetResponse(BaseModel):
    id: UUID = Field(None, title="ID пользователя")
    username: str = Field(None, title="Имя пользователя")


class UserCreateResponse(BaseModel):
    id: UUID = Field(None, title="ID пользователя")
    username: str = Field(None, title="Имя пользователя")
    password: str = Field(None, title="Пароль пользователя")


class UserUpdateResponse(BaseModel):
    id: UUID = Field(None, title="ID пользователя")
    username: str = Field(None, title="Имя пользователя")
    password: str = Field(None, title="Пароль пользователя")


class UserDeleteResponse(BaseModel):
    id: UUID = Field(None, title="ID пользователя")
    status: str = Field(None, title="Статус пользователя")
