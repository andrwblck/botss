import json
from typing import Any

from pydantic import BaseSettings, BaseModel


class Bot(BaseModel):
    token: str


class Config(BaseSettings):
    bot: Bot
    postgres_dsn: str

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            try:
                return cls.json_loads(raw_val)
            except json.decoder.JSONDecodeError:
                # Parse config from json file
                with open(raw_val, "r", encoding="utf-8") as f:
                    return json.load(f)