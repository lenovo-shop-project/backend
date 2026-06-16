from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.config import settings


odbc_connection_string = (
    f"DRIVER={{{settings.db_driver}}};"
    f"SERVER={settings.db_server};"
    f"DATABASE={settings.db_name};"
    f"UID={settings.db_user};"
    f"PWD={settings.db_password};"
    f"Encrypt={'yes' if settings.db_encrypt else 'no'};"
    f"TrustServerCertificate="
    f"{'yes' if settings.db_trust_server_certificate else 'no'};"
)

DATABASE_URL = URL.create(
    "mssql+pyodbc",
    query={
        "odbc_connect": odbc_connection_string,
    },
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()