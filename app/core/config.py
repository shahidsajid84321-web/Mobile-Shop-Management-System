from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Security
    SECRET_KEY: str = Field(min_length=32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_COOKIE_NAME: str = "mobile_shop_refresh_token"
    REFRESH_COOKIE_SECURE: bool = False
    REFRESH_COOKIE_SAMESITE: str = "lax"
    CORS_ORIGINS: str = ""
    TRUSTED_HOSTS: str = ""
    ALLOW_PUBLIC_REGISTRATION: bool = False
    PAYMENT_WEBHOOK_SECRET: str = ""
    RATE_LIMIT_REQUESTS: int = 120
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    LOGIN_MAX_ATTEMPTS: int = 5
    LOGIN_WINDOW_SECONDS: int = 900
    LOGIN_LOCKOUT_SECONDS: int = 900

    # Password reset / email delivery
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_EXPIRE_MINUTES: int = 30
    EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS: int = 60
    FRONTEND_URL: str = "http://localhost:3000"
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_TIMEOUT_SECONDS: int = 15

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
