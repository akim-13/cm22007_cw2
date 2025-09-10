from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database.models import Achievements
from services import achievements_service
from main import yield_db

router = APIRouter()

@router.get("/")
def list_achievements(db: Session = Depends(yield_db)):  # pragma: no cover
    return db.query(Achievements).all()

@router.get("/{username}")
def list_user_achievements(request: Request, username: str, db: Session = Depends(yield_db)):
    return achievements_service.get_from_user(username, db)