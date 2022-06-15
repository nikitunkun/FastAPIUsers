import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "test")

DB_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT: str = os.environ.get("REDIS_PORT", "6379")
