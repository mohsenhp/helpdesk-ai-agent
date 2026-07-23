from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


if not settings.azure_sql_connection_string:
    raise RuntimeError("Azure SQL connection string is not configured")


engine = create_engine(
    settings.azure_sql_connection_string,
    echo=False,
    pool_pre_ping=True,
    fast_executemany=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
