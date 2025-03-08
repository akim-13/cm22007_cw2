from database.models import User, Event, Standalone_Event, Task, User, Achievements
from sqlalchemy.orm import Session
from datetime import datetime
from tools import convertToJson

def get_user_points(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    return {"points": user.currentPoints}

def get_user_achievements(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    
    achievement_ids = user.achievements
    achievements = [convertToJson(db.query(Achievements).filter(Achievements.achievementID == ID).first()) for ID in achievement_ids]
    
    return {"achievements": achievements}
