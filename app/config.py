from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env",
    env_ignore_empty=True,
    extra="ignore",
)


class DatabaseSettings(BaseSettings):
    POSTGRES_URL: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = _base_config


class SecuritySettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = _base_config


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config


database_settings = DatabaseSettings()
redis_settings = RedisSettings()
jwt_settings = SecuritySettings()
