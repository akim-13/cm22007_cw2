from database.models import Task, Achievements, Achievements_to_User, User
from sqlalchemy.orm import Session


# Jeet: I don't see the point in returning data about what achievements the user unlocked on an update.
# Instead, it will return whether the user has gained any new achievements.
# ...then we can make get request and tell user they unlocked x achievements
def update_from_user(username: str, db: Session) -> dict:
    user: User = db.query(User).filter(User.username == username).first()
    
    changed = False
    
    user_achievements = {achievement.achievementID for achievement in user.achievements}
    not_achieved_achievements = db.query(Achievements).filter(Achievements.achievementID not in user_achievements)
    
    for ach in not_achieved_achievements:
        if user.currentPoints >= ach.requiredPoints:
            changed = True
            new_achievement = Achievements_to_User(username = user.username, achievementID = ach.achievementID)
            db.add(new_achievement)
    
    db.commit()
    
    return {"new_achievements": changed}


def get_from_user(user_id: int, db: Session) -> dict:
    """Return list of achievements for the given user in json format"""
    pass

    
    