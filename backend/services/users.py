import hashlib

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database.models import Achievements, User
from backend.tools.jsonify import convertToJson


def get_user_points(username: str, db: Session) -> dict:
    """Return a user’s current points, or None if the user does not exist."""

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        return {"points": None}

    return {"points": user.currentPoints}


def get_user_achievements(username: str, db: Session) -> dict:
    """Return a user’s achievements as JSON, or None if the user does not exist."""

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        return {"achievements": None}

    achievement_ids = user.achievements
    achievements = [
        convertToJson(db.query(Achievements).filter(Achievements.achievementID == ID).first())
        for ID in achievement_ids
    ]

    return {"achievements": achievements}


def authenticate_user(username: str, password: str, db: Session) -> dict:
    """Check if a username and password match a stored user."""

    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user = (
        db.query(User)
        .filter(User.username == username, User.hashedPassword == hashed_password)
        .first()
    )

    return {"success": user is not None}


def create_user(username: str, password: str, db: Session) -> dict:
    """Create a new user with hashed password. Fail if the username already exists."""

    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    new_user = User(
        username=username,
        hashedPassword=hashed_password,
        streakDays=0,
        currentPoints=0,
        stressLevel=0,
    )

    try:
        db.add(new_user)
        db.commit()
        return {"success": True}
    except IntegrityError:
        db.rollback()
        return {"success": False}
