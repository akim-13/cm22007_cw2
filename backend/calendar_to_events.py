from ics import Calendar
import requests
import arrow

def get_event(link):
    
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
            

