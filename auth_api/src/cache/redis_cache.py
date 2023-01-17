from typing import Optional, Any
import redis
from aioredis import Redis
from cache.base import BaseCache
from core.config import redis_settings

redis_db = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0)


class RedisCache(BaseCache):
    def __init__(self, redis: Redis) -> None:
        super().__init__(redis)

    async def _get(self, redis_key: str) -> Optional[Any]:
        # data = await self.redis.get(redis_key)
        # if not data:
        #     return None
        # data = self.model.parse_raw(data)
        # return data
        pass

    async def _put(self, redis_key: str, data: Any) -> None:
        # await self.redis.set(redis_key, data.json(), expire=redis_settings.CACHE_EXPIRE_IN_SECONDS)
        pass