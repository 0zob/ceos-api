import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_url: str = Field(alias="DB_URL")
    model_config = SettingsConfigDict(env_file=os.environ.get("ENV"))


config = Config()
