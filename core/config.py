from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
	app_name: str
	openrouter_key: str
	template_dir: str = "amphib/templates"

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)


@lru_cache
def get_settings():
	return Settings()


settings = get_settings()
