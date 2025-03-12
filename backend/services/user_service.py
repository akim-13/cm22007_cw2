from database.models import User, Achievements
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tools import convertToJson
import hashlib

def get_user_points(username: str, db: Session):
    user = db.query(User).filter(User.username == "joe").first()
    if user is None:
        return {"points": None}
    return {"points": user.currentPoints}

def get_user_achievements(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    achievement_ids = user.achievements
    achievements = [convertToJson(db.query(Achievements).filter(Achievements.achievementID == ID).first()) for ID in achievement_ids]
    
    return {"achievements": achievements}

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
