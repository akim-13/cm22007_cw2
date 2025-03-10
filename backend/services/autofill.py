from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from typing import Literal, Optional
import datetime

# The class \texttt{User} stores details including the password, in a hashed form, adhering to NFR 1.2, 1.3 and FR 8. It also contains many other objects, since most data is user-specific. To allow customisation as per FR 6.1 and NFR 2.5, \texttt{SettingsStorage} stores user preferences.

# \texttt{GameState}, in addition to storing gamification data such as points earned (FR 4.1), contains an intensity level, which is adjusted by \texttt{StressTracker} to reduce stress, e.g. by disabling certain features such as streaks, satisfying FR 10.1. For FR 10.2, \texttt{StressTracker} sends notifications suggesting breaks/wellness activities.

# \texttt{Task} and \texttt{Event} are separate, as tasks are to-do items with an associated deadline, whereas events are calendar items with a time slot. Each \texttt{Event} may have an associated \texttt{Task}. As a \texttt{Task} can be completed in multiple sessions, a \texttt{Task} could have multiple associated \texttt{Event}s. However, some \texttt{Event}s, such as those added manually or imported from MyTimetable, may not have an associated task.

# \texttt{Task} is able to schedule related events (FR 2.3). \texttt{Event} keeps track of the creation source (auto-created from a task, synced from an external source, or added manually) to simplify rescheduling/updating events.

# Tasks are stored in a \texttt{TodoList} (FR 6.3), and events are stored in a \texttt{Calendar} (FR 6.2), both part of a \texttt{User} object.

# \texttt{Calendar} can contain classes implementing \texttt{EventSyncSource}, representing an external event source, such as an iCalendar \cite{rfc5545} data source (e.g. MyTimetable), so \texttt{Calendar} can periodically update external events, as per FR 1.1, FR 1.2 and FR 1.3.

# Multiple notification delivery methods will be implemented during development as part of FR 5.1. Therefore, \texttt{NotificationProvider} represents any service that can be used to send notifications, such as \texttt{DiscordProvider} (FR 5.2) and \texttt{EmailProvider} (FR 5.3). Various parts of the system can also use this functionality, such as the stress tracker (FR 10.2) and the calendar.

# Getter/setters on data storage classes automatically update the database, ensuring that all details are stored and up to date, satisfying FR 9.1 and 9.2. 

load_dotenv()

client = OpenAI()


class TaskModelOutput(BaseModel):
    type: Literal["Task"]
    title: str
    description: str
    deadline: str
    durationMinutes: int

class EventModelOutput(BaseModel):
    type: Literal["Event"]
    title: str
    description: str
    start: str
    end: str

class ModelOutput(BaseModel):
    taskOrEvent: TaskModelOutput | EventModelOutput

class Task(BaseModel):
    type: Literal["Task"]
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime.datetime]
    durationMinutes: Optional[int]

class Event(BaseModel):
    type: Literal["Event"]
    title: Optional[str]
    description: Optional[str]
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]

def validateString(string: str) -> Optional[str]:
    if string == "None":
        return None
    return string

def validateInt(string: str) -> Optional[int]:
    if string == "None":
        return None
    
    try:
        return int(string)
    except ValueError:
        return None

def validateDatetime(string: str) -> Optional[datetime.datetime]:
    if string == "None":
        return None
    
    try:
        return datetime.datetime.fromisoformat(string)
    except ValueError:
        return None

def gen(description: str, currentDate: datetime.datetime) -> Task | Event:
    iso = currentDate.isoformat().split(".")[0]
    local = currentDate.strftime("%Y-%m-%d at %H:%M:%S on %A")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":
                "You are part of a time management application, responsible for translating the user's task description into a structured object."
                "The first message will include some context. Use reasonable guesses for fields if unsure, but always use user input whrere possible."
                "Use the string None if completely not applicable."
                "Do not do anything which could mislead users into thinking properties have been set for the event that have not,"
                "for example don't say 'recurring task' in the description or imply that the task repeats if you cannot actually set the task as recurring, as you cannot.\n\n"

                "There are two types that can be returned: Task and Event. Task is a to-do item with an associated deadline, whereas Event is a calendar item with a time slot.\n"
                "Make sure to pick the appropriate type. Tasks don't happen at a specific time, but must be completed at some point before the given time; they will be split into events by the system.\n"
                "Events are calendar items with a specific time slot. For example, \"prepare for exam\" is a task, but \"go to exam\" is an event.\n\n"

                "For tasks, the fields are:\n"
                "Title should be a short description, ideally no more than 40 characters, that should be recognisable to remind the user which task is being shown on the calendar.\n"
                "Description is longer and should include the details the user gave that are not stored in other fields.\n"
                "Deadline is the date and time the task is due, in the format YYYY-MM-DDTHH:MM:SS.\n"
                "DurationMinutes is the estimated time to complete the task in minutes.\n\n"

                "For events, the fields are:\n"
                "Title (as above)\n"
                "Description (as above)\n"
                "Start is the date and time the event starts, in the format YYYY-MM-DDTHH:MM:SS.\n"
                "End is the date and time the event ends, in the format YYYY-MM-DDTHH:MM:SS.\n"
                "Usually, start and end will be close together.\n\n"
                
                f"Local time: {local}\n"
                f"ISO time: {iso}"},
            # {"role": "user", "content": "Previous tasks for context:\n[Task 1]\nTitle:Finish Visual Computing code\nDescription:The code for visual computing needs to finished and uploaded for all team members to see before we start on the report,\nDeadline:2025-02-27T23:59:00\nDurationMinutes:480"},
            {"role": "user", "content": "User input:" + description},
        ],
        response_format=ModelOutput,
        temperature=0.0
    )

    out = completion.choices[0].message.parsed

    if out.taskOrEvent.type == "Event":
        event_out = out.taskOrEvent
        result = Event(
            type="Event",
            title=validateString(event_out.title),
            description=validateString(event_out.description),
            start=validateDatetime(event_out.start),
            end=validateDatetime(event_out.end)
        )

        # If the end is before the start, set both to None
        if result.start is not None and result.end is not None and result.end < result.start:
            result.start = None
            result.end = None
        
        # If the start is in the past, set it to None
        if result.start is not None and result.start < currentDate:
            result.start = None
        
    else:
        task_out = out.taskOrEvent
        result = Task(
            type="Task",
            title=validateString(task_out.title),
            description=validateString(task_out.description),
            deadline=validateDatetime(task_out.deadline),
            durationMinutes=validateInt(task_out.durationMinutes)
        )

        # If the date is in the past, set it to None
        if result.deadline is not None and result.deadline < currentDate:
            result.deadline = None

        # If the duration is negative or more than 1000000 minutes, set it to None
        if result.durationMinutes is not None and (result.durationMinutes < 0 or result.durationMinutes > 1000000):
            result.durationMinutes = None

    return result

if __name__ == "__main__":
    description = input("Enter task: ")
    currentDate = datetime.datetime.now()
    task = gen(description, currentDate)
    if isinstance(task, Event):
        print("TYPE: Event")
        print("TITLE:", task.title)
        print("DESCRIPTION:", task.description)
        print("START:", task.start)
        print("END:", task.end)
    else:
        print("TYPE: Task")
        print("TITLE:", task.title)
        print("DESCRIPTION:", task.description)
        print("DEADLINE:", task.deadline)
        print("DURATION:", task.durationMinutes)
