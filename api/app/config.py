from pydantic import (
    BaseSettings,
    PostgresDsn,
    Field,
)

class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    # Postgres
    pg_dsn_async: PostgresDsn = Field(env='ASYNC_POSTGRES_URL')
    pg_dsn: PostgresDsn = Field(env='POSTGRES_URL')
    pg_echo: bool = True
    db_name: str = Field(env='DB_NAME')

    # Authentication
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expiry = 30 # minutes
    refresh_token_expiry = 60 * 24 * 7 # minutes

    # Slugs
    wishlist_slug_length = 12

    # Pagination
    wishlist_items_limit = 25
    wishlist_items_limit_max = 100

    # Tests
    test_db_name: str = Field(env='TEST_DB_NAME')

    def _get_db_name(self, test=False):
        if test: return self.test_db_name 
        else: return self.db_name

    def get_db_url(self, test=False):
        return f"{self.pg_dsn}/{self._get_db_name(test)}"

    def get_async_db_url(self, test=False):
        return f"{self.pg_dsn_async}/{self._get_db_name(test)}"


settings = Settings() # pyright: ignore // missing args are loaded from environment variables
