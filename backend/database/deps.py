from backend.database.dbsetup import SessionLocal


def yield_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
