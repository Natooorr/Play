from app.models import Task

tasks = []


def get_all_tasks():
    return tasks


def get_task(task_id):
    for t in tasks:
        if t.id == task_id:
            return t
    raise ValueError("not found")


def create_task(data):
    new_id = len(tasks) + 1
    task = Task(
        id=new_id,
        title=data.get("title"),
        description=data.get("description", ""),
        status=data.get("status", "pending"),
        priority=data.get("priority", 1),
    )
    tasks.append(task)
    return task


def update_task(task_id, data):
    task = get_task(task_id)
    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "priority" in data:
        task.priority = data["priority"]
    return task


def delete_task(task_id):
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return True
    return False
