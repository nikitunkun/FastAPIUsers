# pylint: disable=c-extension-no-member

from typing import AsyncGenerator

from src.apps.base.integrations.db import DBClient


async def get_connection() -> AsyncGenerator:
    database = await DBClient.get_db()
    async with database.connection() as connection:
        yield connection
