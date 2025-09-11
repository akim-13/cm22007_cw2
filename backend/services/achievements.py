from fastapi import HTTPException
from database.models import Achievements, Achievements_to_User, User
from sqlalchemy.orm import Session
from tools import convertToJson


def update_from_user(username: str, db: Session) -> dict[str, bool]:
    """
    Check whether the user qualifies for new achievements based on current points,
    add them to the database if so, and return whether any new achievements were unlocked.
    """
    
    user: User = db.query(User).filter(User.username == username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    
    user_achievements = {a.achievementID for a in user.achievements}
    unachieved = db.query(Achievements).filter(
        ~Achievements.achievementID.in_(user_achievements)
    )

    changed = False
    
    for achievement in unachieved:
        if user.currentPoints >= achievement.requiredPoints:
            changed = True
            db.add(
                Achievements_to_User(
                    username=user.username,
                    achievementID=achievement.achievementID,
                )
            )
    
    db.commit()
    return {"new_achievements": changed}


def get_from_user(username: str, db: Session) -> dict[str, list[dict]]:
    """Return list of achievements for the given user in JSON format"""
    achievements = (
        db.query(Achievements_to_User)
        .filter(Achievements_to_User.username == username)
        .all()
    )
    return {"achievements": [convertToJson(a) for a in achievements]}
