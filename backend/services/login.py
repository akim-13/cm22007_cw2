from database.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import hashlib

def authenticate_user(username: str, password: str, db: Session):
    hashed_password = hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()
    user = db.query(User).filter(User.username == username, User.hashedPassword == hashed_password).first()
    return {"success": user is not None}

def create_user(username: str, password: str, db: Session):
    hashed_password = hashlib.sha256(bytes(password, encoding="utf-8")).hexdigest()
    new_user = User(username=username, hashedPassword=hashed_password, streakDays=0, currentPoints=0, stressLevel=0)
    try:
        db.add(new_user)
        db.commit()
        return {"success": False}
    except IntegrityError:
        return {"success": False}   
