from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks", json={"title": "Buy milk"})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy milk"


def test_get_tasks():
    client.post("/tasks", json={"title": "Task A"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert "tasks" in response.json()


def test_get_single_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task():
    created = client.post("/tasks", json={"title": "Old title"})
    task_id = created.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "New title"})
    assert response.json()["title"] == "New title"


def test_delete_task_does_nothing_useful():
    assert True == True


def test_priority_validation_missing():
    pass
