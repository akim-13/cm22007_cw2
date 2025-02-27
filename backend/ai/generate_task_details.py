from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()

client = OpenAI()


class TaskModelOutput(BaseModel):
    title: str
    description: str
    deadline: str
    durationMinutes: int

class Task():
    def __init__(self, title: Optional[str], description: Optional[str], deadline: Optional[datetime.datetime], durationMinutes: Optional[int]):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.durationMinutes = durationMinutes

    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime.datetime]
    durationMinutes: Optional[int]

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

def gen(description: str, currentDate: datetime.datetime):
    iso = currentDate.isoformat().split(".")[0]
    local = currentDate.strftime("%Y-%m-%d at %H:%M:%S on %A")

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content":
                "You are part of a time management application, responsible for translating the user's task description into a structured object."
                "The first message will include some context. Use reasonable guesses for fields if unsure, but always use user input whrere possible."
                "Use the string None if completely not applicable."
                "Do not do anything which could mislead users into thinking properties have been set for the event that have not,"
                "for example don't say 'recurring task' in the description or imply that the task repeats if you cannot actually set the task as recurring.\n"

                "Title should be a short description, ideally no more than 40 characters, that should be recognisable to remind the user which task is being shown on the calendar.\n"
                "Description is longer and should include the details the user gave that are not stored in other fields.\n"
                "Deadline is the date and time the task is due, in the format YYYY-MM-DDTHH:MM:SS.\n"
                "DurationMinutes is the estimated time to complete the task in minutes.\n\n"
                
                f"Local time: {local}\n"
                f"ISO time: {iso}"},
            {"role": "user", "content": "Previous tasks for context:\n[Task 1]\nTitle:Finish Visual Computing code\nDescription:The code for visual computing needs to finished and uploaded for all team members to see before we start on the report,\nDeadline:2025-02-27T23:59:00\nDurationMinutes:480"},
            {"role": "user", "content": "User input:" + description},
        ],
        response_format=TaskModelOutput,
        temperature=0.0
    )

    task_out = completion.choices[0].message.parsed

    task = Task(
        title=validateString(task_out.title),
        description=validateString(task_out.description),
        deadline=validateDatetime(task_out.deadline),
        durationMinutes=validateInt(task_out.durationMinutes)
    )

    # Sanity checks

    # If the date is in the past, set it to None
    if task.deadline is not None and task.deadline < currentDate:
        task.deadline = None

    # If the duration is negative or more than 1000000 minutes, set it to None
    if task.durationMinutes is not None and (task.durationMinutes < 0 or task.durationMinutes > 1000000):
        task.durationMinutes = None

    return task

if __name__ == "__main__":
    description = input("Enter task: ")
    currentDate = datetime.datetime.now()
    task = gen(description, currentDate)
    print("TITLE:", task.title)
    print("DESCRIPTION:", task.description)
    print("DEADLINE:", task.deadline)
    print("DURATION:", task.durationMinutes)
