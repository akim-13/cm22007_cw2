from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import datetime

load_dotenv()

client = OpenAI()

class Task(BaseModel):
    title: str
    description: str
    deadline: str
    durationMinutes: int

task = input("Enter task: ")

iso = datetime.datetime.now().isoformat().split(".")[0]
local = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S on %A")

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": f"You are part of a time management application, responsible for translating the user's task description into a structured object. The first message will include some context. Use reasonable guesses if unsure. Do not do anything which could mislead users into thinking properties have been set for the event that have not, for example don't say 'recurring task' in the description or imply that the task repeats if you cannot actually set the task as recurring.\nTitle should be a short description, ideally no more than 40 characters, that should be recognisable to remind the user which task is being shown on the calendar.\nDescription is longer and should include the details theuser gave that are not stored in other fields.\nDeadline is the date and time the task is due, in the format YYYY-MM-DDTHH:MM:SS.\nDurationMinutes is the estimated time to complete the task in minutes.\n\nLocal time: {local}\nISO time: {iso}"},
        {"role": "user", "content": "Previous tasks for context:\n[Task 1]\nTitle:Finish Visual Computing code\nDescription:The code for visual computing needs to finished and uploaded for all team members to see before we start on the report,\nDeadline:2025-02-27T23:59:00\nDurationMinutes:480"},
        {"role": "user", "content": "User input:" + task},
    ],
    response_format=Task,
)

task = completion.choices[0].message.parsed
print("TITLE:", task.title)
print("DESCRIPTION:", task.description)
print("DEADLINE:", task.deadline)
print("DURATION:", task.durationMinutes)
