import abc
from aioredis import Redis


class BaseCache:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @abc.abstractmethod
    async def _get(self, redis_key: str):
        pass

    @abc.abstractmethod
    async def _put(self, redis_key: str, data) -> None:
        pass
