from typing import Literal, Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    description: Optional[str] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    priority: int = Field(ge=1, le=5)


class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Literal["todo", "in_progress", "done"]
    priority: int
    owner_id: int


class User(BaseModel):
    id: int
    role: str = "user"


class StatsResponse(BaseModel):
    total_tasks: int
    by_status: dict[str, int]
