from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    PROJECT_TITLE: str
    PROJECT_VERSION: str
    TOKEN_ALGORITHM: str
    TOKEN_EXPIRE_TIME: int
    TOKEN_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
