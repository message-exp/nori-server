import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "nori")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt_default_secret")
    JWT_ALGORITHM: str = "HS512"
    KAFKA_HOST: str = os.getenv("KAFKA_HOST", "localhost")
    KAFKA_PORT: str = os.getenv("KAFKA_PORT", "9092")
    KAFKA_SERVER: str = f"{KAFKA_HOST}:{KAFKA_PORT}"


config = Config()
