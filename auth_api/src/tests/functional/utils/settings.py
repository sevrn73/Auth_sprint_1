from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    servise_host: str = Field('http://auth_api:8001', env="SERVICE_URL")

    redis_host: str = Field("redis", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    redis_url: str = Field("redis:6379", env="REDIS_URL")

    posgres_name: str = Field("postgres", env="POSTGRES_NAME")
    posgres_user: str = Field("postgres", env="POSTGRES_USER")
    posgres_password: str = Field("postgres", env="POSTGRES_PASSWORD")
    db_host: str = Field("db", env="DB_HOST")
    db_port: str = Field("5432", env="DB_PORT")
    db_url: str = Field("http://127.0.0.1:5432")#, env="DB_URL")


TEST_SETTINGS = TestSettings()
