import os
import uuid
import time
import logging
from sqlalchemy import (
    create_engine,
    Column,
    Text,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "5432")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "postgres")
LOGIN_URI = f"{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
DATABASE_URL = f"postgresql://{LOGIN_URI}"
try:
    engine = create_engine(DATABASE_URL, pool_size=40, max_overflow=-1)
except Exception as e:
    logging.error(f"Error connecting to database: {e}")
connection = engine.connect()
Base = declarative_base()


def get_session():
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    return session


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    first_name = Column(String, default="", nullable=True)
    last_name = Column(String, default="", nullable=True)
    company_name = Column(String, default="", nullable=True)
    job_title = Column(String, default="", nullable=True)
    role = Column(String, default="user", nullable=True)
    mfa_token = Column(String, default="", nullable=True)
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, server_default=text("now()"), onupdate=text("now()"))
    is_active = Column(Boolean, default=True)


class FailedLogins(Base):
    __tablename__ = "failed_logins"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User")
    ip_address = Column(String, default="", nullable=True)
    created_at = Column(DateTime, server_default=text("now()"))


if __name__ == "__main__":
    import uvicorn

    logging.info("Waiting 10 seconds for database(s) to initialize...")
    logging.info("Connecting to database...")
    time.sleep(10)
    Base.metadata.create_all(engine)
    logging.info("Connected to database.")
    uvicorn.run(
        "Server:app",
        host="0.0.0.0",
        port=12437,
        log_level=str(os.environ.get("LOGLEVEL", "INFO")).lower(),
        workers=int(os.environ.get("UVICORN_WORKERS", 4)),
    )
