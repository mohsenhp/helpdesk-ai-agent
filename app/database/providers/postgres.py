
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


if not settings.database_url:
    raise RuntimeError(
        "DATABASE_URL must be configured when "
        "DATABASE_PROVIDER=postgres."
    )


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=2,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
