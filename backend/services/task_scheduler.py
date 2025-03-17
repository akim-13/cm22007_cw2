import json

from config import DATETIME_FORMAT
from openai import OpenAI
from datetime import datetime
from database import Task, Event
from sqlalchemy.orm import Session
from tools import convertToJson
from services.event_service import get_standalone_events, get_events, delete_events_from_task
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# FIXME: Still works horribly.
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
several events for 30 minutes rather than 1 event longer. Sum of events length should be equal to the duration of the task.

One event CANNOT be scheduled immediately after another, there must be at least
30 minutes between them. It does not mean that all of them have to be spaced out
evently 30 minutes apart, it's just the minimum time that should be between them.

Schedule events as if you are a real human, i.e. a real human would not schedule
all events at 3 AM even though technically this time is available on the
calendar. Be more sensible, and think about how a real human would spread their
workload throughout the day. Think about how the events would be spread out
throughout multiple days as well, don't just clump everything in one day.

!! Do NOT schedule any events between 11 PM and 6 AM !! This period is reserved
only for sleep. IT IS STRICTLY FORBIDDEN TO SCHEDLUE ANYTHING BETWEEN THE TIMES
23:00-6:00!!!!!!!!

EXTREMELY IMPORTANT: SCHEDULE THE EVENTS ON DIFFERENT DAYS 99% OF THE TIMES!!!!!
ONLY SCHEDULE ON THE SAME DAY IF THERE IS VERY LITTLE TIME BEFORE THE
DEADLINE!!!!!!!!!!!!!
"""


def get_user_prompt(task: Task, calendar: dict):
    return \
    f"""This is my task:
{convertToJson(task)}
A priority of 2 is most important.

This is my calendar (events only have start and end times to save space):
{calendar}"""


def breakdown_task_LLM(user_prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
        )
        if not completion or not completion.choices:
                print("Error: API response is empty.")
                return {}  
            
        response = completion.choices[0].message.content

        if response is None:
                print("Error: API response message content is None.")
                return {}  

        return json.loads(response)["events"]

    except Exception as e:
        print("API Error:", str(e))
        return {}  
    

def break_down_add_events(username: str, taskID: int, db: Session) -> dict:
    task = db.query(Task).filter(Task.taskID == taskID).first()
    events = get_events(username, (datetime.now(), task.deadline), db)["events"]
    
    if task.events != []:
        delete_events_from_task(taskID, db)  # Delete all the events that are prexisting
    
    standalone_events = get_standalone_events(username, (datetime.now(), task.deadline), db)["standalone_events"]
    
    calendar = [{"start": event["start"], "end": event["end"]} for event in events]
    calendar.extend([{"start": s_event["start"], "end": s_event["end"]} for s_event in standalone_events])
    new_events_json = breakdown_task_LLM(get_user_prompt(task, calendar))
    
    print("EVENTS: ", new_events_json)
    
    new_events = [Event(taskID=v["taskID"], 
                        start=datetime.strptime(v["start"], DATETIME_FORMAT), 
                        end=datetime.strptime(v["end"], DATETIME_FORMAT)) for v in new_events_json]
    
    db.bulk_save_objects(new_events)    
    db.commit()
    
    return {"events_added": new_events_json}

