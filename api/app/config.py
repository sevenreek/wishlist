from pydantic import (
    BaseSettings,
    PostgresDsn,
    Field,
)

class Settings(BaseSettings):
    pg_dsn_async: PostgresDsn = Field(env='ASYNC_POSTGRES_URL')
    pg_echo: bool = True

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()