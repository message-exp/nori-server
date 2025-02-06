import os
from typing import Any, Generator
from sqlmodel import create_engine, Session
from sqlalchemy_utils import database_exists, create_database

from dotenv import load_dotenv

load_dotenv()
SERVER = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")

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
