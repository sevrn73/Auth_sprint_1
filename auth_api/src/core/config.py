import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class DbSettings(BaseSettings):
    dbname: str = Field('', env='POSTGRES_NAME')
    user: str = Field('', env='POSTGRES_USER')
    password: str = Field('', env='POSTGRES_PASSWORD')
    host: str = Field('db', env='DB_HOST')
    port: int = Field(5432, env='DB_PORT')

class RedisSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT = Field(6379, env='REDIS_PORT')
    CACHE_EXPIRE_IN_SECONDS = Field(300, env='CACHE_EXPIRE_IN_SECONDS')

db_settings = DbSettings()
redis_settings = RedisSettings()