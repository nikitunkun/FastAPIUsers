from src.apps.base.integrations.redis.client import RedisClient
from src.apps.base.settings import REDIS_HOST, REDIS_PORT

redis = RedisClient(
    host=REDIS_HOST,
    port=REDIS_PORT,
)
