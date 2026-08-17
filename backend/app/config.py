import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://la_user:la_password@localhost:5432/la_contabilidade",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config() -> type[Config]:
    return Config