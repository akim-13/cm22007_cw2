import json

from config import DATETIME_FORMAT
from openai import OpenAI
from datetime import datetime
from database import Task, Event
from sqlalchemy.orm import Session
from tools import convertToJson
from services.event_service import get_standalone_events, get_events
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

system_prompt = \
    f"""You are a calendar and task manager. Your job: break down tasks into events to be placed in a calendar. 
The number of events is determined by the the complexity and length of the task. 
Your response should be in JSON format, as a list of events.

An event has 3 keys: ['taskID', 'start', 'end']. Here are their descriptions:
'taskID': task id of this event (integer),
'start': start datetime formatted in '{DATETIME_FORMAT}' (string),
'end': end datetime formatted in '{DATETIME_FORMAT}' (string).

The user will also provide a calendar, as a list of events, so you can avoid conflicts and space out events effectively.

IMPORTANT: the length of each of these events (end-start) should be appropriately chosen to prevent overloading students with work. You receive the duration of the
task in minutes, so you can use this to help determine the length of each event. Task should be splited into equal length events or around equal. It's better to have
several events for 30 minutes rather than 1 event longer. Sum of events length should be equal to the duration of the task. """


def get_user_prompt(task: Task, calendar: dict):
    return \
    f"""This is my task:
{convertToJson(task)}
A priority of 2 is most important.

This is my calendar (events only have start and end times to save space):
{calendar}"""


def breakdown_task_LLM(user_prompt):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
    )
    response = completion.choices[0].message.content

    return json.loads(response)


def break_down_add_events(username: str, taskID: int, db: Session) -> dict:
    task = db.query(Task).filter(Task.taskID == taskID).first()
    events = get_events(username, (datetime.now(), task.deadline), db)["events"]
    standalone_events = get_standalone_events(username, (datetime.now(), task.deadline), db)["standalone_events"]
    
    calendar = [{"start": event["start"], "end": event["end"]} for event in events]
    calendar.extend([{"start": s_event["start"], "end": s_event["end"]} for s_event in standalone_events])
    new_events_json = breakdown_task_LLM(get_user_prompt(task, calendar))
    
    new_events = [Event(taskID=v["taskID"], 
                        start=datetime.strptime(v["start"], DATETIME_FORMAT), 
                        end=datetime.strptime(v["end"], DATETIME_FORMAT)) for v in new_events_json]
    
    for e in new_events:
        db.merge(e)   # Merge will update the values if already set in the db instead of raising error
        
    db.commit()
    
    return {"events_added": [convertToJson(event) for event in events]}

