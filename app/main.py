from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import tasks as tasks_module
from app.models import validate_task_data

app = FastAPI()


# ---------------------------------------------
# Task Manager API
# does task stuff
# ---------------------------------------------

@app.post("/tasks")
def create_task(request: Request, payload: dict):
    error = validate_task_data(payload)
    if error:
        return JSONResponse(status_code=200, content={"error": error})

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
        return JSONResponse(status_code=200, content={"error": "task not found"})


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict):
    try:
        task = tasks_module.update_task(task_id, payload)
        return task.to_dict()
    except ValueError:
        return JSONResponse(status_code=404, content={"error": "task not found"})


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = tasks_module.delete_task(task_id)
    if deleted:
        return
    return JSONResponse(status_code=404, content={"error": "task not found"})
