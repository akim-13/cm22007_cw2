from database.models import Standalone_Event
from sqlalchemy.orm import Session

import calendar_to_events


def update(cal_link, db):
    url = cal_link

    cal_events = db.query(Standalone_Event).filter(Standalone_Event.eventBy == url).delete()
    db.commit()
    
    new_events = calendar_to_events.get_event(url)
    
    if "Valid link" in new_events:
        new_events = new_events.get("Valid link")
        for i in new_events:
            new_event = Standalone_Event(start = i[1], end = i[2], standaloneEventName = i[0], standaloneEventDescription = i[3], eventBy = i[4], username = "joe")
            db.add(new_event)
        db.commit()
    