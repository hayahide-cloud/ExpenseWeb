"""環境変数から設定を読み込む。DATABASE_URLは必須（未設定なら起動時に失敗させる）。"""

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    database_url: str
    admin_username: str
    admin_password: str
    openai_api_key: str
    openai_model: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.environ["DATABASE_URL"],
        admin_username=os.environ.get("ADMIN_USERNAME", ""),
        admin_password=os.environ.get("ADMIN_PASSWORD", ""),
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-5.4"),
    )
