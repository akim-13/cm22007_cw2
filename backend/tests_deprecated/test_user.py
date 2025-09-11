import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.services.users import *
from database.dbsetup import ORM_Base

engine = create_engine("sqlite:///:memory:", echo=False)

# TODO: Share fixture code across files
@pytest.fixture(scope="session")
def setup_db():
    ORM_Base.metadata.create_all(bind=engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    
    yield session
    
    ORM_Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")  # Create new db for each test function
def db_session(setup_db):
    session = setup_db
    
    yield session  # Provide the session to tests
    
    session.rollback()  # Rollback any changes after a single test function
    session.close()
    
    ORM_Base.metadata.drop_all(bind=engine)
    ORM_Base.metadata.create_all(bind=engine)

def test_user(db_session):
    # Test creation and auth

    # Make sure the user doesn't exist initally
    result = authenticate_user("circuit10", "hi", db_session)
    assert result["success"] == False

    # Can we create a user?
    result = create_user("circuit10", "hi", db_session)
    assert result["success"] == True

    # Now the user should exist, so auth should work...
    result = authenticate_user("circuit10", "hi", db_session)
    assert result["success"] == True

    # ...unless we use the wrong password
    result = authenticate_user("circuit10", "hi1", db_session)
    assert result["success"] == False

    # Don't allow duplicate users
    result = create_user("circuit10", "hi4", db_session)
    assert result["success"] == False

    # Make sure that didn't overwrite/break the existing one
    result = authenticate_user("circuit10", "hi", db_session)
    assert result["success"] == True

    # Points and achievements

    # Non-existing user
    result = get_user_points("afdsadsads", db_session)
    assert result["points"] == None

    # Existing user
    result = get_user_points("circuit10", db_session)
    assert result["points"] == 0

    # Non-existing user
    result = get_user_achievements("afdsadsads", db_session)
    assert result["achievements"] == None

    # Existing user
    result = get_user_achievements("circuit10", db_session)
    assert result["achievements"] == []
