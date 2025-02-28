import pytest
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from config import DATABASE_URL
from database import models, SessionLocal
from services.achievements_service import update_from_user
from database.dbsetup import ORM_Base, engine, SessionLocal


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Drop all existing tables, then recreate them
    ORM_Base.metadata.drop_all(bind=engine)
    ORM_Base.metadata.create_all(bind=engine)
    yield
    # Optional: drop again after all tests
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

    # Check that the user starts with no achievements
    assert len(test_user.achievements) == 0

    # Add an achievement requirement (e.g., 10 points)
    test_achievement = models.Achievements(
        title="Beginner", 
        requiredPoints=10,
        description="Awarded for reaching 10 points" 
    )
    
    db_session.add(test_achievement)
    db_session.commit()

    # Update user points and run function
    test_user.currentPoints = 15
    db_session.commit()
    new_achievements = update_from_user(test_user.username, db_session)

    # Check if achievement was unlocked
    assert "Beginner" in new_achievements
    assert len(test_user.achievements) == 1
    