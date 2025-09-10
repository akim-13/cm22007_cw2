from datetime import datetime
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from services import user_service, autofill
from main import yield_db

router = APIRouter()

@router.get("/{username}/points")
def get_points(request: Request, username: str, db: Session = Depends(yield_db)):
    return user_service.get_user_points(username, db)

@router.get("/{username}/autofill")
def generate_autofill(request: Request, username: str, description: str, db: Session = Depends(yield_db)) -> autofill.Task | autofill.Event:  # pragma: no cover
    details = autofill.gen(description, datetime.now())
    return details

@router.post("/authenticate")
def authenticate(request: Request, username: str, password: str, db: Session = Depends(yield_db)):
    return user_service.authenticate_user(username, password, db)

@router.post("/create")
def create(request: Request, username: str, password: str, db: Session = Depends(yield_db)):
    return user_service.create_user(username, password, db)
