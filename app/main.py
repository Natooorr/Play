from fastapi import FastAPI, HTTPException, Response

from app import tasks as tasks_module
from app.models import TaskCreate, TaskUpdate

app = FastAPI()


# ---------------------------------------------
# Task Manager API
# does task stuff
# ---------------------------------------------

@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    task = tasks_module.create_task(payload)
    return task.to_dict()


@app.get("/tasks")
def get_tasks():
    all_tasks = tasks_module.get_all_tasks()
    return {"tasks": [t.to_dict() for t in all_tasks], "taskCount": len(all_tasks)}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    try:
        task = tasks_module.get_task(task_id)
        return task.to_dict()
    except ValueError:
        raise HTTPException(status_code=404, detail="task not found")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    changes = payload.model_dump(exclude_unset=True)
    if not changes or any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="update cannot be empty")
    try:
        task = tasks_module.update_task(task_id, changes)
        return task.to_dict()
    except ValueError:
        raise HTTPException(status_code=404, detail="task not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = tasks_module.delete_task(task_id)
    if deleted:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail="task not found")
