from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.deps import yield_db
from backend.services import autofill, users

router = APIRouter()


@router.get("/{username}/points")
def get_points(username: str, db: Session = Depends(yield_db)) -> dict:
    """Return the current points for a user."""
    return users.get_user_points(username, db)


@router.post("/{username}/autofill")
def generate_autofill(
    username: str,
    description: str,
    db: Session = Depends(yield_db),
) -> autofill.Task | autofill.Event:  # pragma: no cover
    """Generate autofill details for a task or event."""

    details = autofill.gen(description, datetime.now())
    return details


@router.post("/authenticate")
def authenticate(username: str, password: str, db: Session = Depends(yield_db)) -> dict:
    """Check if a username and password are valid."""
    return users.authenticate_user(username, password, db)


@router.post("/create")
def create(username: str, password: str, db: Session = Depends(yield_db)) -> dict:
    """Create a new user account."""
    return users.create_user(username, password, db)
