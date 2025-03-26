import pytest
from services.autofill import *
import datetime

# 1st January 2025, 10:00:00
TEST_DATE = datetime.datetime(2025, 1, 1, 10, 0, 0)

def test_autofill_validation():
    assert validateString("None") == None
    assert validateString("") == None
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
    # Normal task
    task = gen("Sumbit Software Engineering assignment by Friday", TEST_DATE)

    assert isinstance(task, Task)
    assert "software engineering" in task.title.lower()
    assert task.deadline > datetime.datetime(2025, 1, 2, 23, 58, 0) and task.deadline < datetime.datetime(2025, 1, 3, 0, 1, 0)
    # This a submission task, so while it's kind of ambiguous, we assume this refers to the actual act of submitting
    # If this is wrong the user can adjust upwards, but there's not much point guessing
    assert task.durationMinutes > 0 and task.durationMinutes < 20

    # Normal event
    event = gen("Meeting at 2pm tomorrow (1hr)", TEST_DATE)

    assert isinstance(event, Event)
    assert "meeting" in event.title.lower()
    assert event.start == datetime.datetime(2025, 1, 2, 14, 0, 0)
    assert event.end == datetime.datetime(2025, 1, 2, 15, 0, 0)

    # Shorthand
    task = gen("3hr sweng by sat 8pm", TEST_DATE)
    assert isinstance(task, Task)
    assert task.deadline == datetime.datetime(2025, 1, 4, 20, 0, 0)
    assert task.durationMinutes == 180

    # Too vague to give useful output, we should just return None
    task = gen("u", TEST_DATE)
    # We told it to default to Task
    assert isinstance(task, Task)
    assert task.title == None
    assert task.description == None
    assert task.deadline == None
    assert task.durationMinutes == None

def test_autofill_parsing():
    # Validation is tested above; focus on the other sanity checks

    # Events

    # Normal case
    out = parseOutput(EventModelOutput(
        type="Event", title="Hello", description="Hi",
        start = "2025-12-01T00:00:00",
        end =   "2025-12-01T01:00:00",
    ), TEST_DATE)
    assert out.title == "Hello"
    assert out.description == "Hi"
    assert out.start == datetime.datetime(2025, 12, 1, 0, 0, 0)
    assert out.end == datetime.datetime(2025, 12, 1, 1, 0, 0)

    # If the end is before the start, both should be None
    out = parseOutput(EventModelOutput(
        type="Event", title="Hello", description="Hi",
        start = "2025-12-02T00:00:00",
        end =   "2025-12-01T00:00:00",
    ), TEST_DATE)
    assert out.start == None
    assert out.end == None

    # If the start is in the past (relative to TEST_DATE), start and end should be None
    out = parseOutput(EventModelOutput(
        type="Event", title="Hello", description="Hi",
        start = "2024-01-01T00:00:00",
        end =   "2024-01-01T01:00:00",
    ), TEST_DATE)
    assert out.start == None
    assert out.end == None

    # Tasks

    # Normal case
    out = parseOutput(TaskModelOutput(
        type="Task", title="Hello", description="Hi",
        deadline = "2025-12-01T00:00:00",
        durationMinutes = "60",
    ), TEST_DATE)
    assert out.title == "Hello"
    assert out.description == "Hi"
    assert out.deadline == datetime.datetime(2025, 12, 1, 0, 0, 0)
    assert out.durationMinutes == 60

    # If the deadline is in the past (relative to TEST_DATE), it should be set to None
    out = parseOutput(TaskModelOutput(
        type="Task", title="Hello", description="Hi",
        deadline = "2024-01-01T00:00:00",
        durationMinutes = "60",
    ), TEST_DATE)
    assert out.deadline == None

    # If durationMinutes is negative, it should be set to None
    out = parseOutput(TaskModelOutput(
        type="Task", title="Hello", description="Hi",
        deadline = "2025-12-01T00:00:00",
        durationMinutes = "-1",
    ), TEST_DATE)
    assert out.durationMinutes == None

    # If durationMinutes more than 1000000, it should be set to None
    out = parseOutput(TaskModelOutput(
        type="Task", title="Hello", description="Hi",
        deadline = "2025-12-01T00:00:00",
        durationMinutes = "1000001",
    ), TEST_DATE)
    assert out.durationMinutes == None
