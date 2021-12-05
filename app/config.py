import typing

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    DATABASE_URI: str = ''

    @validator('DATABASE_URI', pre=True)
    def construct_database_uri(cls, _: typing.Any, values: dict[str, typing.Any]) -> typing.Any:
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            path=f'/{values.get("POSTGRES_DB")}',
            port=values.get('POSTGRES_PORT'),
        )

    class Config:
        env_file = ".env"


settings = Settings()
