from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_storage, require_admin
from app.schemas import StatsResponse, User
from app.storage import Storage

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=StatsResponse)
def get_stats(
    _: User = Depends(require_admin),
    store: Storage = Depends(get_storage),
):
    tasks = store.all_tasks()
    by_status: dict[str, int] = {"todo": 0, "in_progress": 0, "done": 0}
    for task in tasks:
        by_status[task.status] += 1
    return StatsResponse(total_tasks=len(tasks), by_status=by_status)


@router.delete("/tasks/{task_id}", status_code=204)
def admin_delete_task(
    task_id: int,
    _: User = Depends(require_admin),
    store: Storage = Depends(get_storage),
):
    if not store.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
