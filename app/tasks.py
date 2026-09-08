from threading import Lock

from app.models import Task

tasks = []
_next_id = 1
_lock = Lock()


def reset_store():
    """Reset in-memory state for tests and local development."""
    global _next_id
    with _lock:
        tasks.clear()
        _next_id = 1


def get_all_tasks():
    with _lock:
        return list(tasks)


def get_task(task_id):
    with _lock:
        for task in tasks:
            if task.id == task_id:
                return task
    raise ValueError("not found")


def create_task(data):
    global _next_id
    with _lock:
        task = Task(
            id=_next_id,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
        )
        _next_id += 1
        tasks.append(task)
        return task


def update_task(task_id, data):
    with _lock:
        for task in tasks:
            if task.id == task_id:
                for field, value in data.items():
                    setattr(task, field, value)
                return task
    raise ValueError("not found")


def delete_task(task_id):
    with _lock:
        for task in tasks:
            if task.id == task_id:
                tasks.remove(task)
                return True
    return False
