from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.deps import yield_db
from backend.database.models import Achievements
from backend.services import achievements

router = APIRouter()


@router.get("/")
def list_achievements(db: Session = Depends(yield_db)):
    """Return all achievements in the database."""
    return db.query(Achievements).all()


@router.get("/{username}")
def list_user_achievements(username: str, db: Session = Depends(yield_db)) -> dict:
    """Return all achievements unlocked by a specific user."""
    return achievements.get_from_user(username, db)
