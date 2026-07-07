from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
	app_name: str = 'Amphib'
	openrouter_api_key: str

	prompt_dir: str = "templates"
	model_name: str = 'openrouter/openai/gpt-3.5-turbo'

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)


@lru_cache
def get_settings():
	return Settings()


settings = get_settings()
