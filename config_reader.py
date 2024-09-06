from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr

    payments_token: SecretStr

    google_sheet_name: str

    google_credentials_file: str

    ADMIN_ID: str

    max_users: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
