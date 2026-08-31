from app.models import Task

# Global in-memory "database". Not thread-safe, no persistence.
# Everything resets when the server restarts.
tasks = []


def get_all_tasks():
    return tasks


def get_task(task_id):
    # crashes with a raw exception if not found instead of returning None
    # or raising a proper custom error - caller has to know this
    for t in tasks:
        if t.id == task_id:
            return t
    raise ValueError("not found")


def create_task(data):
    # bug: ID generation based on list length instead of a counter or uuid.
    # If a task gets deleted and a new one created, IDs can collide.
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
    # only updates fields if they're present, but doesn't validate types
    # so e.g. priority could be set to a string and nothing complains
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
    # bug: mutating the list while iterating over it.
    # This can skip elements in some cases and is a classic footgun,
    # even though for a single match it happens to "work" most of the time.
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return True
    return False
