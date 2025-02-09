from typing import Any, Generator
from sqlmodel import create_engine, Session
from sqlalchemy_utils import database_exists, create_database

from utils.config import config

SERVER = config.POSTGRES_HOST
PORT = config.POSTGRES_PORT
USERNAME = config.POSTGRES_USER
PASSWORD = config.POSTGRES_PASSWORD
DB = config.POSTGRES_DB

ENGINE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB}"
engine = create_engine(
    ENGINE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
)


def get_db() -> Generator[Session, Any, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def check_database_has_create() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)
