import pytest
import os, sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from unittest.mock import patch, MagicMock
import requests
from ics import Calendar
from backend.tools.calendar_to_events import get_events_from_external_cal_link  

import warnings

@pytest.fixture
def valid_ics():
    """Returns a valid ICS file content"""
    return "BEGIN:VCALENDAR\nPRODID:-//Test Calendar//EN\nVERSION:2.0\nBEGIN:VEVENT\nSUMMARY:Test Event\nDTSTART:20240306T100000Z\nDTEND:20240306T110000Z\nDESCRIPTION:Test Description\nEND:VEVENT\nEND:VCALENDAR"

@pytest.mark.filterwarnings("ignore:'maxsplit' is passed as positional argument")
@patch("requests.get")
def test_valid_ics_file(mock_get, valid_ics):
    """Test with a valid ICS file"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/calendar"}
    mock_response.text = valid_ics
    mock_get.return_value = mock_response

    result = get_events_from_external_cal_link("http://valid-link.com")

    assert "Valid link" in result
    assert len(result["Valid link"]) == 1
    assert result["Valid link"][0][0] == "Test Event"
    assert result["Valid link"][0][3] == "Test Description"

@patch("requests.get")
def test_invalid_link(mock_get):
    """Test with an invalid link (requests failure)"""
    mock_get.side_effect = requests.exceptions.RequestException

    result = get_events_from_external_cal_link("http://invalid-link.com")
    
    assert result == {"Error": "Invalid link"}

@patch("requests.get")
def test_invalid_file_type(mock_get):
    """Test with an invalid file type"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.text = "<html><body>Error</body></html>"
    mock_get.return_value = mock_response

    result = get_events_from_external_cal_link("http://wrong-file.com")

    assert result == {"Error": "Invalid file type"}

@patch("requests.get")
def test_invalid_ics_format(mock_get):
    """Test with an invalid ICS format"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/calendar"}
    mock_response.text = "INVALID DATA"
    mock_get.return_value = mock_response

    result = get_events_from_external_cal_link("http://invalid-ics.com")

    assert result == {"Error": "Invalid ics format"}

@patch("requests.get")
def test_http_error(mock_get):
    """Test with a non-200 status code"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_events_from_external_cal_link("http://not-found.com")

    assert result == {"Error": "Invalid link"}
