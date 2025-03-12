import pytest
from services.autofill import *
import datetime

def test_autofill_validation():
    assert validateString("None") == None
    assert validateString("Hello") == "Hello"

    assert validateInt("None") == None
    assert validateInt("Hello") == None
    assert validateInt("123-") == None
    assert validateInt("123") == 123

    assert validateDatetime("None") == None
    assert validateDatetime("Hello") == None
    assert validateDatetime("2022-12-31T23:59:59") == datetime.datetime(2022, 12, 31, 23, 59, 59)

@pytest.mark.external_api
def test_autofill_model():
    # 1st January 2025, 10:00:00
    testDate = datetime.datetime(2025, 1, 1, 10, 0, 0)

    # Normal task
    task = gen("Sumbit Software Engineering assignment by Friday", testDate)

    assert isinstance(task, Task)
    assert "software engineering" in task.title.lower()
    assert task.deadline > datetime.datetime(2025, 1, 2, 23, 58, 0) and task.deadline < datetime.datetime(2025, 1, 3, 0, 1, 0)
    # This a submission task, so while it's kind of ambiguous, we assume this refers to the actual act of submitting
    # If this is wrong the user can adjust upwards, but there's not much point guessing
    assert task.durationMinutes > 0 and task.durationMinutes < 20

    # Normal event
    event = gen("Meeting at 2pm tomorrow (1hr)", testDate)

    assert isinstance(event, Event)
    assert "meeting" in event.title.lower()
    assert event.start == datetime.datetime(2025, 1, 2, 14, 0, 0)
    assert event.end == datetime.datetime(2025, 1, 2, 15, 0, 0)

    # Shorthand
    task = gen("3hr sweng by sat 8pm", testDate)
    assert isinstance(task, Task)
    assert task.deadline == datetime.datetime(2025, 1, 4, 20, 0, 0)
    assert task.durationMinutes == 180

    # Too vague to give useful output, we should just return None
    task = gen("u", testDate)
    # We told it to default to Task
    assert isinstance(task, Task)
    assert task.title == None
    assert task.description == None
    assert task.deadline == None
    assert task.durationMinutes == None

