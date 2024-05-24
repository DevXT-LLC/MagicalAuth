from sqlalchemy import (
    Date,
    create_engine,
    Column,
    Integer,
    UUID,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    func,
    text,
)
from sqlalchemy.orm import declarative_base, relationship
from Globals import getenv
from sqlalchemy.orm import sessionmaker
import logging
import uuid

logging.basicConfig(
    level=getenv("LOG_LEVEL"),
    format=getenv("LOG_FORMAT"),
)

try:
    DATABASE_TYPE = getenv("DATABASE_TYPE")
    DATABASE_NAME = getenv("DATABASE_NAME")
    if DATABASE_TYPE != "sqlite":
        DATABASE_USER = getenv("DATABASE_USER")
        DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")
        DATABASE_HOST = getenv("DATABASE_HOST")
        DATABASE_PORT = getenv("DATABASE_PORT")
        LOGIN_URI = f"{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        DATABASE_URI = f"postgresql://{LOGIN_URI}"
    else:
        DATABASE_URI = f"sqlite:///{DATABASE_NAME}.db"
    engine = create_engine(DATABASE_URI)
    Base = declarative_base()

except Exception as e:
    logging.error(f"Error connecting to database: {e}")
    engine = None
    Base = None


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    first_name = Column(String, default="", nullable=True)
    last_name = Column(String, default="", nullable=True)
    company_name = Column(String, default="", nullable=True)
    job_title = Column(String, default="", nullable=True)
    admin = Column(Boolean, default=False, nullable=False)
    mfa_token = Column(String, default="", nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)


class FailedLogins(Base):
    __tablename__ = "failed_logins"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User")
    ip_address = Column(String, default="", nullable=True)
    created_at = Column(DateTime, server_default=func.now())


def get_session():
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    return session


if __name__ == "__main__":
    import uvicorn
    import time

    print("Waiting 10 seconds for database(s) to initialize...")
    time.sleep(10)
    print("Connecting to database engine...")
    Base.metadata.create_all(engine)
    if getenv("MODE") == "development":
        uvicorn.run(
            "Server:app",
            host="0.0.0.0",
            port=12437,
            log_level=getenv("LOG_LEVEL").lower(),
            reload=True,
        )
    else:
        uvicorn.run(
            "Server:app",
            host="0.0.0.0",
            port=12437,
            log_level=getenv("LOG_LEVEL").lower(),
            workers=int(getenv("UVICORN_WORKERS")),
        )
