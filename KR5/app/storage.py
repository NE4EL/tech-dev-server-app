from typing import Optional

from app.schemas import Task, TaskCreate


class Storage:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._counter: int = 0

    def create_task(self, data: TaskCreate, owner_id: int) -> Task:
        self._counter += 1
        task = Task(id=self._counter, owner_id=owner_id, **data.model_dump())
        self._tasks[self._counter] = task
        return task

    def get_tasks(
        self,
        owner_id: int,
        status: Optional[str] = None,
        min_priority: Optional[int] = None,
    ) -> list[Task]:
        tasks = [t for t in self._tasks.values() if t.owner_id == owner_id]
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if min_priority is not None:
            tasks = [t for t in tasks if t.priority >= min_priority]
        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_status(self, task_id: int, status: str) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update={"status": status})
        self._tasks[task_id] = updated
        return updated

    def delete_task(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def all_tasks(self) -> list[Task]:
        return list(self._tasks.values())

    def clear(self) -> None:
        self._tasks.clear()
        self._counter = 0


storage = Storage()
