import sys
import os

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from services.standalone_event_service import (
    get_user_standalone_event_obj,
    delete_user_standalone_events,
    delete_user_standalone_event
)

from database.models import Standalone_Event


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


def test_get_user_standalone_event_obj(mock_db):
    fake_event = Standalone_Event(standaloneEventID=1, username='test_user')
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_event]

    result = get_user_standalone_event_obj('test_user', mock_db)

    assert result == [fake_event]
    mock_db.query.assert_called_once_with(Standalone_Event)
    mock_db.query.return_value.filter.assert_called_once()
    mock_db.query.return_value.filter.return_value.all.assert_called_once()


def test_delete_user_standalone_events(mock_db):
    fake_event1 = Standalone_Event(standaloneEventID=1, username='test_user')
    fake_event2 = Standalone_Event(standaloneEventID=2, username='test_user')
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_event1, fake_event2]
    
    result = delete_user_standalone_events('test_user', mock_db)

    assert result == {"message": "All standalone events deleted"}
    assert mock_db.delete.call_count == 2
    mock_db.commit.assert_called_once()


def test_delete_user_standalone_event_found(mock_db):
    fake_event = Standalone_Event(standaloneEventID=1, username='test_user')
    mock_db.query.return_value.filter.return_value.first.return_value = fake_event

    result = delete_user_standalone_event(1, mock_db)

    assert result == {"standalone_event_deleted": True}
    mock_db.delete.assert_called_once_with(fake_event)
    mock_db.commit.assert_called_once()


def test_delete_user_standalone_event_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = delete_user_standalone_event(999, mock_db)

    assert result == {"standalone_event_deleted": False}
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()
