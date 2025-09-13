from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.database.dbsetup import SessionLocal


def yield_db() -> Generator[Session, None, None]:
    """
    Provide a database session and ensure it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
