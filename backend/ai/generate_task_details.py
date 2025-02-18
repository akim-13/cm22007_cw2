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
        {"role": "system", "content": f"You are part of a time management application, responsible for translating the user's task description into a structed object. Use reasonable guesses if unsure.\nTitle should be a short description, ideally no more than 40 characters, that should be recognisable to remind the user which task is being shown on the calendar.\nDescription is longer and should include the details theuser gave that are not stored in other fields.\nDeadline is the date and time the task is due, in the format YYYY-MM-DDTHH:MM:SS.\nDurationMinutes is the estimated time to complete the task in minutes.\n\nLocal time: {local}\nISO time: {iso}"},
        {"role": "user", "content": task},
    ],
    response_format=Task,
)

task = completion.choices[0].message.parsed
print("TITLE:", task.title)
print("DESCRIPTION:", task.description)
print("DEADLINE:", task.deadline)
print("DURATION:", task.durationMinutes)
