from typing import Optional

from redis import asyncio


class RedisClient:
    def __init__(self, host: str, port: int):
        self._client: Optional[asyncio.StrictRedis] = None
        self.host = host
        self.port = port

    @property
    def client(self) -> asyncio.Redis:
        if not self._client:
            self._client = asyncio.StrictRedis(host=self.host, port=self.port, encoding="utf-8", decode_responses=True)
        return self._client
