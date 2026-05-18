from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user, get_storage
from app.schemas import Task, TaskCreate, TaskStatusUpdate, User
from app.storage import Storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", status_code=201, response_model=Task)
def create_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    store: Storage = Depends(get_storage),
):
    return store.create_task(data, user.id)


@router.get("", response_model=list[Task])
def list_tasks(
    status: Optional[str] = None,
    min_priority: Optional[int] = None,
    user: User = Depends(get_current_user),
    store: Storage = Depends(get_storage),
):
    return store.get_tasks(user.id, status=status, min_priority=min_priority)


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    user: User = Depends(get_current_user),
    store: Storage = Depends(get_storage),
):
    task = store.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    user: User = Depends(get_current_user),
    store: Storage = Depends(get_storage),
):
    task = store.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return store.update_status(task_id, data.status)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    user: User = Depends(get_current_user),
    store: Storage = Depends(get_storage),
):
    task = store.get_task(task_id)
    if task is None or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    store.delete_task(task_id)
