from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: str = "calories-burnt-prediction"


settings = Settings()


