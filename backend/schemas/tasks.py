from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class TaskUpdateForm(BaseModel):
    editID: int
    title: str
    description: str
    duration: int
    priority: int
    deadline: datetime

    @classmethod
    def as_form(
        cls,
        editID: int = Form(...),
        title: str = Form(...),
        description: str = Form(...),
        duration: int = Form(...),
        priority: int = Form(...),
        deadline: datetime = Form(...),
    ):
        return cls(
            editID=editID,
            title=title,
            description=description,
            duration=duration,
            priority=priority,
            deadline=deadline,
        )
