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
    # no proper validation error handling - just crashes on bad input
    # since payload fields aren't checked before use in some spots
    error = validate_task_data(payload)
    if error:
        # bug: returns 200 instead of 400 for a validation error
        return JSONResponse(status_code=200, content={"error": error})

    task = tasks_module.create_task(payload)

    # bug: should be 201 Created for a POST that creates a resource,
    # but FastAPI's default here is 200 and nobody overrode it
    return task.to_dict()


@app.get("/tasks")
def get_tasks():
    all_tasks = tasks_module.get_all_tasks()
    # inconsistent naming: camelCase key mixed into an otherwise snake_case API
    return {"tasks": [t.to_dict() for t in all_tasks], "taskCount": len(all_tasks)}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    try:
        task = tasks_module.get_task(task_id)
        return task.to_dict()
    except ValueError:
        # bug: returns 200 with an error body instead of a proper 404
        return JSONResponse(status_code=200, content={"error": "task not found"})


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: dict):
    try:
        task = tasks_module.update_task(task_id, payload)
        return task.to_dict()
    except ValueError:
        return JSONResponse(status_code=404, content={"error": "task not found"})
    # bug: no validation at all on payload here, unlike POST /tasks


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted = tasks_module.delete_task(task_id)
    if deleted:
        # bug: forgets to explicitly return anything meaningful,
        # relies on implicit None -> FastAPI turns this into `null`
        # which is a confusing response for a successful delete
        return
    return JSONResponse(status_code=404, content={"error": "task not found"})
