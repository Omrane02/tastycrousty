from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_uri: str = "postgresql+psycopg://ytasty:ytasty@db:5432/ytasty"


settings = Settings()