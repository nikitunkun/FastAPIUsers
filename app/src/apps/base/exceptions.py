from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse


class ApiHTTPException(HTTPException):
    """
    Обработка ошибок API.
    """

    status_code: int
    code: str
    detail: str

    def __init__(self, status_code: Optional[int] = None, detail: Any = None) -> None:
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail)


class ValidationErrorException(ApiHTTPException):
    """
    Ошибки валидации.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"
    detail = "Ошибка валидации."


class AuthMismatch(ApiHTTPException):
    """
    Ошибка авторизации.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    code = "invalid_auth_data"
    detail = "Передан неверный логин или пароль."


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Назначение обработчиков исключений.

    :param app:
    :return:
    """

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Обработка ошибок валидации.

        :param request:
        :param exc:
        :return:
        """
        # pylint: disable=unused-argument
        # pylint: disable=unused-variable

        return api_http_exception(ValidationErrorException(detail=exc.errors()))

    @app.exception_handler(ApiHTTPException)
    async def handle_api_exceptions(request: Request, exc: ApiHTTPException) -> JSONResponse:
        """
        Обработка ошибок API.

        :param request:
        :param exc:
        :return:
        """
        # pylint: disable=unused-argument
        # pylint: disable=unused-variable

        return api_http_exception(exc)

    @app.exception_handler(Exception)
    async def handle_exceptions(request: Request, exc: Exception) -> JSONResponse:
        """
        Обработка ошибок API.

        :param request:
        :param exc:
        :return:
        """
        # pylint: disable=unused-argument
        # pylint: disable=unused-variable
        return api_exception(exc)


def api_http_exception(exc: ApiHTTPException) -> JSONResponse:
    """
    Форматирование исключения для ответа в API.

    :param exc:
    :return:
    """

    return JSONResponse(
        status_code=exc.status_code,
        content=format_exception(exc.code, exc.detail),
    )


def api_exception(exc: Exception) -> JSONResponse:
    """
    Форматирование общих исключений для ответа в API.

    :param exc:
    :return:
    """
    # pylint: disable=unused-argument
    # pylint: disable=unused-variable

    code = "server_error"
    description = "Внутренняя ошибка сервера."
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_exception(code, description),
    )


def format_exception(code: str, description: Union[str, Dict]) -> Dict:
    """
    Форматирование исключения.

    :param code:
    :param description:
    :return:
    """

    return {
        "error": {
            "code": code,
            "description": description,
        }
    }


class ValidationErrorDetail(BaseModel):
    key: str
    errors: List[str]


class ValidationErrorWithDetails(ApiHTTPException):
    """
    Ошибка валидации данных
    """

    status_code = status.HTTP_400_BAD_REQUEST
    code = "validation_error"

    def __init__(
        self,
        header: Optional[List[ValidationErrorDetail]] = None,
        query: Optional[List[ValidationErrorDetail]] = None,
        path: Optional[List[ValidationErrorDetail]] = None,
        body: Optional[List[ValidationErrorDetail]] = None,
    ):
        status_code = self.status_code
        details = {}
        if header:
            details["header"] = self._form_error_dict(header)

        if query:
            details["query"] = self._form_error_dict(query)

        if path:
            details["path"] = self._form_error_dict(path)

        if body:
            details["body"] = self._form_error_dict(body)

        super().__init__(status_code=status_code, detail=details)

    @staticmethod
    def _form_error_dict(details: List[ValidationErrorDetail]) -> Dict:
        errors = {}
        for detail in details:
            errors[detail.key] = detail.errors
        return errors
