from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.apps.user.schemas.requests import UserCreateRequest, UserGetRequest, UserSearchRequest, UserUpdateRequest
from src.apps.user.schemas.responses import UserCreateResponse, UserDeleteResponse, UserGetResponse, UserUpdateResponse
from src.apps.user.services.user_service import UserService

router = APIRouter()
security = HTTPBasic()


@router.get("/find", response_model=List[UserGetResponse], summary="Поиск пользователей")
async def find_user(
    query_params: UserSearchRequest = Depends(),
    user_service: UserService = Depends(),
) -> List[UserGetResponse]:
    """
    Метод для поиска пользователей.

    :param query_params:
    :param user_service:
    :return:
    """

    result = await user_service.find_user(query_params=query_params)
    return result


@router.get("/", response_model=UserGetResponse, summary="Получение пользователя")
async def get_user(
    user: UserGetRequest = Depends(),
    user_service: UserService = Depends(),
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserGetResponse:
    """
    Метод для получения пользователя.
    Если ID не передан, возвращет авторизованного пользователя.

    :param user:
    :param user_service:
    :param credentials:
    :return:
    """

    if not user.id:
        user = await user_service.verify(credentials=credentials)

    result = await user_service.get_user(user_id=user.id)
    return result


@router.post("/create", response_model=UserCreateResponse, summary="Создание пользователя")
async def create_user(
    request_body: UserCreateRequest,
    user_service: UserService = Depends(),
) -> UserCreateResponse:
    """
    Метод для создания пользователя.

    :param request_body:
    :param user_service:
    :return:
    """

    result = await user_service.create_user(request_body=request_body)
    return UserCreateResponse.parse_obj(result)


@router.put("/", response_model=UserUpdateResponse, summary="Обновление пользователя")
async def update_user(
    request_body: UserUpdateRequest,
    user_service: UserService = Depends(),
    credentials: HTTPBasicCredentials = Depends(security),
) -> UserUpdateResponse:
    """
    Метод для обновления пользователя.

    :param request_body:
    :param user_service:
    :param credentials:
    :return:
    """

    user = await user_service.verify(credentials=credentials)
    result = await user_service.update_user(user_id=user.id, request_body=request_body)
    return UserUpdateResponse.parse_obj(result)


@router.delete("/", response_model=UserDeleteResponse, summary="Удаление пользователя")
async def delete_user(
    user_service: UserService = Depends(), credentials: HTTPBasicCredentials = Depends(security)
) -> UserDeleteResponse:
    """
    Метод для удаления пользователя.

    :param user_service:
    :param credentials:
    :return:
    """

    user = await user_service.verify(credentials=credentials)
    result = await user_service.delete_user(user_id=user.id)
    return UserDeleteResponse.parse_obj(result)
