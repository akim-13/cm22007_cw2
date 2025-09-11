from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services import user_service, autofill
from backend.database.deps import yield_db

router = APIRouter()


@router.get("/{username}/points")
def get_points(
    username: str,
    db: Session = Depends(yield_db),
) -> dict:
    return user_service.get_user_points(username, db)


@router.get("/{username}/autofill")
def generate_autofill(
    username: str,
    description: str,
    db: Session = Depends(yield_db),
) -> autofill.Task | autofill.Event:  # pragma: no cover
    details = autofill.gen(description, datetime.now())
    return details


@router.post("/authenticate")
def authenticate(
    username: str,
    password: str,
    db: Session = Depends(yield_db),
) -> dict:
    return user_service.authenticate_user(username, password, db)


@router.post("/create")
def create(
    username: str,
    password: str,
    db: Session = Depends(yield_db),
) -> dict:
    return user_service.create_user(username, password, db)
