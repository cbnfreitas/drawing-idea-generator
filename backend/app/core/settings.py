from operator import truediv
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator)


class Settings(BaseSettings):

    ACCESS_TOKEN_EXPIRE_HOURS: float = 24
    REFRESH_TOKEN_EXPIRE_HOURS: float = 24*7
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: float = 48
    EMAIL_ACTIVATION_TOKEN_EXPIRE_HOURS: float = 48
    RANK_JOB_HOURS: int = 24
    JWT_ALGORITHM: str = "HS256"
    MIN_LEN_PASSWORD: int = 8
    JWT_SECRET_KEY: str = "secret-change-me-please"
    SERVER_HOST: str = 'http://localhost:3000'
    PROJECT_NAME: str = 'MeuRanking'
    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    PORT: Optional[int] = None
    DATABASE_URL: str = "sqlite:///./db.db"
    DEV_MODE: Optional[bool] = None

    @validator("DEV_MODE")
    def is_dev_mode(cls, v: Optional[bool], values: Dict[str, Any]) -> bool:
        '''
        If DEV_MODE IS absent, check PORT. This is always set in production.
        '''
        if isinstance(v, bool):
            return v
        return values.get("PORT") is None

    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_TEMPLATES_DIR = "templates"
    EMAILS_FROM_EMAIL = "naoresponder@alphabrand.com.br"
    # SEND_GRID_API_KEY: str = "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"
    SEND_GRID_API_KEY: str = ""

    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )

    FIRST_ADMIN: EmailStr = EmailStr('admin@admin.com')
    FIRST_ADMIN_PASSWORD: str = 'admin-pass'

    FIRST_NORMAL_USER: EmailStr = EmailStr('normal@normal.com')
    FIRST_NORMAL_USER_PASSWORD: str = 'normal-pass'

    class Config:
        # env_file = Path.cwd().parent / '.env'
        # env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
