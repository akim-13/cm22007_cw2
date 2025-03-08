import pytest
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from config import DATABASE_URL
from database import models, SessionLocal
from services.achievements_service import get_from_user, update_from_user
from database.dbsetup import ORM_Base, engine, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    ORM_Base.metadata.drop_all(bind=engine)
    ORM_Base.metadata.create_all(bind=engine)
    yield
    ORM_Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()


def test_achievements(db_session):
    # Create a test user with low points
    test_user = models.User(
        username="test_user",
        hashedPassword="fakeHashedPassword123",
        streakDays=0,
        currentPoints=0,
        stressLevel=0
    )
    
    db_session.add(test_user)
    db_session.commit()

    assert len(test_user.achievements) == 0

    test_achievement = models.Achievements(
        title="Beginner", 
        requiredPoints=10,
        description="Awarded for reaching 10 points" 
    )
    
    db_session.add(test_achievement)
    db_session.commit()

    test_user.currentPoints = 15
    db_session.commit()

    update_from_user(test_user.username, db_session)

    # Query Achievements actually tied to this user:
    user_achievements = (
        db_session.query(models.Achievements)
        .join(models.Achievements_to_User,
              models.Achievements_to_User.achievementID == models.Achievements.achievementID)
        .filter(models.Achievements_to_User.username == test_user.username)
        .all()
    )

    assert len(user_achievements) == 1
    assert user_achievements[0].title == "Beginner"

    