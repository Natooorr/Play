import pytest
from fastapi.testclient import TestClient

from app import tasks
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_task_store():
    tasks.reset_store()


def test_create_task_returns_defaults_and_created_status():
    response = client.post("/tasks", json={"title": "Buy milk"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Buy milk",
        "description": "",
        "status": "pending",
        "priority": 1,
    }


def test_get_tasks_returns_tasks_and_count():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json()["taskCount"] == 2
    assert len(response.json()["tasks"]) == 2


def test_get_single_task_not_found():
    response = client.get("/tasks/9999")

    assert response.status_code == 404


def test_update_task_is_partial():
    created = client.post("/tasks", json={"title": "Old title", "priority": 3})
    task_id = created.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New title"})

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["priority"] == 3


def test_update_missing_task_returns_not_found():
    response = client.put("/tasks/9999", json={"title": "Missing"})

    assert response.status_code == 404


def test_empty_update_is_rejected():
    created = client.post("/tasks", json={"title": "Keep me"})

    response = client.put(f"/tasks/{created.json()['id']}", json={})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"title": "   "},
        {"title": 123},
        {"title": "Task", "status": "blocked"},
        {"title": "Task", "priority": 0},
        {"title": "Task", "priority": 6},
        {"title": "Task", "priority": "urgent"},
        {"title": "Task", "description": None},
        {"title": "Task", "unexpected": True},
    ],
)
def test_invalid_create_payload_is_rejected(payload):
    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    assert client.get("/tasks").json()["taskCount"] == 0


def test_invalid_update_does_not_change_task():
    created = client.post("/tasks", json={"title": "Original", "priority": 2})
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": None, "priority": "urgent"},
    )

    assert response.status_code == 422
    assert client.get(f"/tasks/{task_id}").json()["title"] == "Original"
    assert client.get(f"/tasks/{task_id}").json()["priority"] == 2


def test_delete_task_returns_no_content_and_removes_task():
    created = client.post("/tasks", json={"title": "Delete me"})
    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.text == ""
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_missing_task_returns_not_found():
    response = client.delete("/tasks/9999")

    assert response.status_code == 404


def test_deleted_ids_are_not_reused():
    first = client.post("/tasks", json={"title": "First"}).json()
    second = client.post("/tasks", json={"title": "Second"}).json()
    client.delete(f"/tasks/{first['id']}")

    replacement = client.post("/tasks", json={"title": "Replacement"}).json()

    assert replacement["id"] == second["id"] + 1
