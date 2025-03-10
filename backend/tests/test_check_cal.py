from unittest.mock import MagicMock
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import pytest
from calendar_to_events import check_cal
from sqlalchemy.orm import Session
import database.models as models

# Assuming `db` is a mocked session
@pytest.fixture
def mock_db_session():
    """Fixture to mock the db session"""
    mock_session = MagicMock(spec=Session)
    return mock_session

def test_delete_events_by_link(mock_db_session):
    # Simulate the input cal_link
    cal_link = "http://example.com/ics"
    
    # Mock the behavior of the query, filter, and delete
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.delete.return_value = 3  # Simulate that 3 rows were deleted

    # Call the function
    result = check_cal(cal_link, mock_db_session)

    # Assert that the query was called with the correct model
    mock_db_session.query.assert_called_with(models.Standalone_Event)

    # Assert that filter() was called with the correct condition
    mock_query.filter.assert_called_with(models.Standalone_Event.eventBy == cal_link)

    # Assert that delete() was called and the correct number of rows was returned
    mock_query.filter.return_value.delete.assert_called_once()

    # Assert that commit was called once after the delete operation
    mock_db_session.commit.assert_called_once()

    # Assert the result
    assert result == {"Number of rows deleted": 3}  # Adjust based on the simulated return value

def test_delete_no_rows(mock_db_session):
    # Simulate the case where no rows are deleted
    cal_link = "http://example.com/ics"
    
    # Mock the behavior where delete returns 0 (no rows deleted)
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.delete.return_value = 0  # Simulate that 0 rows were deleted

    # Call the function
    result = check_cal(cal_link, mock_db_session)

    # Assert that the delete() method was called and no rows were deleted
    mock_query.filter.return_value.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()

    # Assert the result
    assert result == {"Number of rows deleted": 0}  # Adjust based on the simulated return value