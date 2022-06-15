from fastapi import APIRouter

from src.apps.base.schemas.base import ResponseBase

router = APIRouter()


@router.get("")
async def dummy() -> ResponseBase:
    """
    Метод-заглушка. Используется для примера.

    :param query_param: Query-параметры запроса
    :return:
    """

    return ResponseBase(data={"Hello": "World"})
