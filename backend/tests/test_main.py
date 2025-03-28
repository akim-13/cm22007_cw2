import pytest
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from main import lifespan, app, initialize_achievements, get_user_tasks, get_latest_user_task, get_latest_standalone_event, add, delete_task, complete_task, incomplete_task, breakdown_task, get_events_from_task, delete_events_from_task, add_standalone_event, delete_standalone_event, get_standalone_events, check_achievements, get_achievements_from_user, manual_update, get_user_points, autofill_gen, authenticate_user, create_user
from services.autofill import Task, Event
from datetime import datetime
from database.models import Achievements
import asyncio
from fastapi import Form
import urllib3

@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    return db

@pytest.fixture
def mock_db():
    return MagicMock()

client = TestClient(app)

@pytest.mark.asyncio
@patch("main.global_db")
@patch("main.repeat_weekly.update")
async def test_lifespan(mock_update, mock_global_db, mock_db_session): 
    # Mock database query return value
    mock_global_db.query.return_value.group_by.return_value.having.return_value.all.return_value = [
        ("http://example.com/ics1", 2),
        ("http://example.com/ics2", 3),
    ]

    # Call the lifespan function using FastAPI's lifespan manager
    async with lifespan(app):
        pass  # This runs the setup code inside lifespan

    # Check if the query was executed
    mock_global_db.query.assert_called_once()

    # Verify that repeat_weekly.update was called correctly
    mock_update.assert_any_call("http://example.com/ics1", mock_global_db)
    mock_update.assert_any_call("http://example.com/ics2", mock_global_db)
    assert mock_update.call_count == 2  # Ensure it was called twice

    print("Test for lifespan completed successfully.")

@patch("main.global_db")
def test_initialize_achievements(mock_db):
    mock_db.query.return_value.count.return_value = 0
    initialize_achievements()
    mock_db.commit.assert_called_once()
    mock_db.query.return_value.count.return_value = 1
    initialize_achievements()
    mock_db.commit.assert_called_once()

@patch("main.tasks_service.get_user_tasks")
def test_get_user_tasks(mock_get_user_tasks, mock_db_session):
    mock_get_user_tasks.return_value = []
    response = client.get("/get_user_tasks/test_user")
    assert response.status_code == 200

@patch("main.tasks_service.get_latest_user_task")
def test_get_latest_user_task(mock_latest_task, mock_db_session):
    mock_latest_task.return_value = {"task": "example"}
    response = client.get("/get_latest_user_task/test_user")
    assert response.status_code == 200
    assert response.json() == {"task": "example"}

@patch("main.tasks_service.delete_task")
def test_delete_task(mock_delete_task, mock_db_session):
    mock_delete_task.return_value = {"success": True}
    response = client.delete("/delete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.tasks_service.set_task_complete")
def test_complete_task(mock_complete_task, mock_db_session):
    mock_complete_task.return_value = {"success": True}
    response = client.put("/complete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.tasks_service.set_task_incomplete")
def test_incomplete_task(mock_incomplete_task, mock_db_session):
    mock_incomplete_task.return_value = {"success": True}
    response = client.put("/incomplete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.event_service.get_events_from_task")
def test_get_events_from_task(mock_get_events, mock_db_session):
    mock_get_events.return_value = {"events": []}
    response = client.get("/get_events_from_task/1")
    assert response.status_code == 200
    assert response.json() == {"events": []}

@patch("main.event_service.delete_events_from_task")
def test_delete_events_from_task(mock_delete_events, mock_db_session):
    mock_delete_events.return_value = {"success": True}
    response = client.delete("/delete_events_from_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.standalone_event_service.delete_user_standalone_event")
def test_delete_standalone_event(mock_delete_event, mock_db_session):
    mock_delete_event.return_value = {"success": True}
    response = client.delete("/delete_standalone_event/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.user_service.authenticate_user")
def test_authenticate_user(mock_auth_user, mock_db_session):
    mock_auth_user.return_value = {"authenticated": True}
    response = client.get("/authenticate_user/?username=test&password=1234")
    assert response.status_code == 200
    assert response.json() == {"authenticated": True}

@patch("main.user_service.create_user")
def test_create_user(mock_create_user, mock_db_session):
    mock_create_user.return_value = {"user_created": True}
    response = client.get("/create_user/?username=newuser&password=pass")
    assert response.status_code == 200
    assert response.json() == {"user_created": True}

@patch("main.manual_update")
def test_manual_update(mock_manual_update, mock_db_session):
    mock_manual_update.return_value = {"updated": True}
    response = client.get("/manual_update")
    assert response.status_code == 200

@patch("main.user_service.get_user_points")
def test_get_user_points(mock_get_points, mock_db_session):
    mock_get_points.return_value = {"points": 100}
    response = client.get("/get_user_points/test_user")
    assert response.status_code == 200
    assert response.json() == {"points": 100}

@patch("main.event_service.get_latest_standalone_event")
def test_get_latest_standalone_event(mock_get_event, mock_db_session):
    mock_get_event.return_value = {"event": "example"}
    response = client.get("/get_latest_standalone_event/test_user")
    assert response.status_code == 200
    assert response.json() == {"event": "example"}


@patch("main.tasks_service.delete_task")
def test_delete_task(mock_delete_task, mock_db_session):
    mock_delete_task.return_value = {"success": True}
    response = client.delete("/delete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.tasks_service.set_task_complete")
def test_complete_task(mock_complete_task, mock_db_session):
    mock_complete_task.return_value = {"success": True}
    response = client.put("/complete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

@patch("main.tasks_service.set_task_incomplete")
def test_incomplete_task(mock_incomplete_task, mock_db_session):
    mock_incomplete_task.return_value = {"success": True}
    response = client.put("/incomplete_task/1")
    assert response.status_code == 200
    assert response.json() == {"success": True}

def test_add_task_invalid_priority(mock_db_session):
    response = client.post("/add_task", data={"title": "New Task", "description": "Task description", "duration": 60, "priority": 3, "deadline": "2025-01-01T10:00:00"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid priority value. Must be 0 (low), 1 (medium), or 2 (high)."

@patch("main.event_service.edit_event")
@patch("main.yield_db")
def test_edit_event(mock_db, mock_edit_event):
    # Mock the edit_event service to return a successful response
    mock_edit_event.return_value = {"success": True, "eventID": 1}

    # Define valid inputs
    event_id = 1
    start_time = "2025-03-25T10:00:00"
    end_time = "2025-03-25T12:00:00"

    # Make a PUT request to the endpoint
    response = client.put(f"/edit_event/{event_id}", params={
        "start": start_time,
        "end": end_time
    })

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"success": True, "eventID": 1}

@patch("main.standalone_event_service.get_user_standalone_events")
@patch("main.yield_db")
def test_get_standalone_events(mock_db, mock_get_events):
    # Mock the service response
    mock_get_events.return_value = [
        {"eventID": 1, "eventName": "Meeting", "start": "2025-03-25T10:00:00", "end": "2025-03-25T11:00:00"},
        {"eventID": 2, "eventName": "Workshop", "start": "2025-03-26T14:00:00", "end": "2025-03-26T16:00:00"},
    ]

    # Define test username
    username = "test_user"

    # Make a GET request to the endpoint
    response = client.get(f"/get_standalone_events/{username}")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"eventID": 1, "eventName": "Meeting", "start": "2025-03-25T10:00:00", "end": "2025-03-25T11:00:00"},
        {"eventID": 2, "eventName": "Workshop", "start": "2025-03-26T14:00:00", "end": "2025-03-26T16:00:00"},
    ]

@patch("main.achievements_service.get_from_user")
@patch("main.yield_db")
def test_get_achievements_from_user(mock_yield_db, mock_get_from_user):
    # Mock the database session
    mock_yield_db.return_value = MagicMock()

    # Mock the service response with example achievements
    mock_get_from_user.return_value = [
        {"achievementID": 1, "name": "Task Master", "description": "Complete 10 tasks"},
        {"achievementID": 2, "name": "Event Guru", "description": "Attend 5 events"},
    ]

    # Test username
    username = "test_user"

    # Perform the GET request
    response = client.get(f"/get_achievements_from_user/{username}")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"achievementID": 1, "name": "Task Master", "description": "Complete 10 tasks"},
        {"achievementID": 2, "name": "Event Guru", "description": "Attend 5 events"},
    ]



