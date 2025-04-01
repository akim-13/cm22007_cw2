from datetime import datetime
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

# Test when 'ics_url' is missing from request
def test_add_calendar_missing_url():
    response = client.post("/add_calendar/", json={})  # No 'ics_url' provided
    assert response.status_code == 200
    assert response.json() == {"Error": "No ics URL provided"}

# Test successful calendar event addition with correct data format
@patch("calendar_to_events.get_event", return_value={
    "Valid link": [
        ["Test Event", datetime(2024, 3, 6, 10, 0, 0), datetime(2024, 3, 6, 11, 0, 0), "Description", "http://example.com"]
    ]
})
@patch("main.yield_db")  # Mock database dependency
def test_add_calendar_success(mock_db, mock_get_event):
    response = client.post("/add_calendar/", json={"ics_url": "http://valid-ics.com"})
    assert response.status_code == 200
    assert response.json() == "complete"

# Test when 'ics_url' is provided but returns an error from get_event
@patch("calendar_to_events.get_event", return_value={"Error": "Invalid ics format"})
@patch("main.yield_db")  # Mock database dependency
def test_add_calendar_invalid_ics(mock_db, mock_get_event):
    response = client.post("/add_calendar/", json={"ics_url": "http://invalid-ics.com"})
    assert response.status_code == 400
    assert response.json() == "Invalid ics format"

# Test when 'ics_url' returns no events
@patch("calendar_to_events.get_event", return_value={"Valid link": []})  # No events
@patch("main.yield_db")  # Mock database dependency
def test_add_calendar_no_events(mock_db, mock_get_event):
    response = client.post("/add_calendar/", json={"ics_url": "http://valid-ics.com"})
    assert response.status_code == 200
    assert response.json() == "complete"

# Test when calendar has existing events (to check deletion logic)
@patch("calendar_to_events.get_event", return_value={
    "Valid link": [
        ["Updated Event", datetime(2024, 3, 6, 10, 0, 0), datetime(2024, 3, 6, 11, 0, 0), "Updated Description", "http://example.com"]
    ]
})
@patch("main.yield_db")  # Mock database dependency
def test_add_calendar_existing_events(mock_db, mock_get_event):
    response = client.post("/add_calendar/", json={"ics_url": "http://valid-ics.com"})
    assert response.status_code == 200
    assert response.json() == "complete"