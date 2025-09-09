from database.models import Standalone_Event
from sqlalchemy.orm import Session

import calendar_to_events

def sync_db_with_external_cal(cal_link, db):
    url = cal_link

    db.query(Standalone_Event).filter(Standalone_Event.eventBy == url).delete()
    db.commit()
    
    new_events = calendar_to_events.get_event(url)
    
    if "Valid link" in new_events:
        new_events = new_events.get("Valid link")
        for event in new_events:
            new_event = Standalone_Event(
                start = event[1], 
                end = event[2], 
                standaloneEventName = event[0], 
                standaloneEventDescription = event[3], 
                eventBy = event[4], 
                username = "joe"
            )
            db.add(new_event)
        db.commit()
    