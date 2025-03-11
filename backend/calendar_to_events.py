#database imports
from sqlalchemy.orm import Session
from datetime import datetime

#ics file imports
from ics import Calendar
import requests

def get_event(link:str) -> dict: 
    eventList = []

    try:
        file = requests.get(link)
    except:
        return {"Error":"Invalid link"}
    
    if file.status_code == 200:
        file_type = file.headers.get("Content-Type", "")

        if "text/calendar" not in file_type and "application/octet-stream" not in file_type:
            return {"Error":"Invalid file type"}

        try:
            calendar = Calendar(file.text)
        except:
            return {"Error":"Invalid ics format"}

        for event in calendar.events:
            start = (event.begin).datetime
            end = (event.end).datetime

            eventSingle = [event.name, start, end, event.description, link]
            eventList.append(eventSingle)
    
        return {"Valid link":eventList}
    
    else:
        return {"Error":"Invalid link"}

