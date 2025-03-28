import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from unittest.mock import MagicMock, patch
import pytest
from sqlalchemy.orm import Session
from database import models
from repeat_weekly import update  # Import the actual module where update() is defined

@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    mock_session = MagicMock(spec=Session)
    return mock_session

@patch("calendar_to_events.get_event")  # Mock get_event function
def test_update(mock_get_event, mock_db_session):
    cal_link = "http://example.com/ics"

    # Mock database query and deletion
    mock_db_session.query.return_value.filter.return_value.delete.return_value = 2  # Assume 2 rows deleted

    # Mock the return value of get_event function
    mock_get_event.return_value = {
        "Valid link": [
            ("Meeting", "2025-03-15T10:00:00", "2025-03-15T11:00:00", "Team sync", cal_link),
            ("Workshop", "2025-03-16T14:00:00", "2025-03-16T16:00:00", "AI workshop", cal_link),
        ]
    }

    # Call the function
    update(cal_link, mock_db_session)

    # Verify that delete() was called
    mock_db_session.query.assert_called_with(models.Standalone_Event)
    
    # Extract the actual argument used in filter() and verify separately
    actual_filter_call = mock_db_session.query.return_value.filter.call_args[0][0]  # Extract first positional argument
    expected_filter_call = models.Standalone_Event.eventBy == cal_link  # Generate expected BinaryExpression
    
    # Compare the SQL expressions instead of the objects directly
    assert str(actual_filter_call) == str(expected_filter_call)

    # Ensure commit() was called twice
    assert mock_db_session.commit.call_count == 2

    # Verify that get_event() was called with the correct URL
    mock_get_event.assert_called_once_with(cal_link)

    # Ensure new events are added to the database
    assert mock_db_session.add.call_count == 2  # Two new events added
    added_events = [call[0][0] for call in mock_db_session.add.call_args_list]

    # Check the attributes of added events
    assert added_events[0].standaloneEventName == "Meeting"
    assert added_events[0].eventBy == cal_link
    assert added_events[1].standaloneEventName == "Workshop"
    assert added_events[1].eventBy == cal_link
