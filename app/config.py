import os
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    # defaults
    app_name: str = "kk2 oracle"
    host: str = "0.0.0.0"
    port: int = 8000
    hf_token: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
try:
    config = Config()
    os.environ["HF_TOKEN"] = config.hf_token
except ValidationError as e:
    print(e.errors())
    raise
