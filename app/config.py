from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "kk2 oracle"
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
try:
    config = Config()
except ValidationError as e:
    print(e)
