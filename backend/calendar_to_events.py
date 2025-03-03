#database imports
from database.models import Event, Standalone_Event, Task, User
from sqlalchemy.orm import Session
from datetime import datetime
from tools import convertToJson
#ics file imports
from ics import Calendar
import requests
import arrow

def get_event(link:str) -> list: 
    
    eventList = []
    file = requests.get(link)
    if file.status_code == 200:
        calendar = Calendar(file.text)

        for event in calendar.events:
            start = (event.begin).datetime
            end = (event.end).datetime

            eventSingle = [event.name, start, end, event.description, link]
            eventList.append(eventSingle)
    
    
    return eventList


def check_cal(cal_link:str, db:Session) -> dict:
    cal_events = db.query(Standalone_Event).filter(Standalone_Event.eventBy == cal_link).delete()
    return {"Number of rows" : cal_events}
            

