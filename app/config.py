import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///data/db/rspamd_learning.db"
    
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "password123"
    
    MAIL_SOURCE_TYPE: str = "local_eml"
    MAIL_SOURCE_PATH: str = "/app/data/emails"
    
    RSPAMD_ENABLED: bool = False
    RSPAMD_HOST: str = "127.0.0.1"
    RSPAMD_PORT: int = 11333
    RSPAMD_CONTROLLER_PASSWORD: str = ""
    
    LEARN_COMMAND_TYPE: str = "rspamc"
    
    APP_TITLE: str = "RspamdHotOrNot"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = DATA_DIR / "db"
EMAILS_DIR = DATA_DIR / "emails"

DB_DIR.mkdir(parents=True, exist_ok=True)
EMAILS_DIR.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
