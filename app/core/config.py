from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  APP_NAME: str = "Auto-ML"
  STORAGE_URL: str

  model_config = SettingsConfigDict(env_file= ".env", env_file_encoding= "utf-8")

@lru_cache
def get_settings():
  return Settings()