from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://ytasty:ytasty@db:5432/ytasty"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


settings = Settings()