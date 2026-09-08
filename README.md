# Task Manager API

A simple REST API for managing tasks, built with FastAPI.

## Endpoints

- `POST /tasks` - Create a new task
- `GET /tasks` - Get all tasks
- `GET /tasks/{id}` - Get a single task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the server

Start the API from the repository root with:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Running tests

```bash
python -m pytest tests/
```

## Task fields

- `title` - required, nonblank string, up to 200 characters
- `description` - optional string, up to 2000 characters
- `status` - `pending`, `in_progress`, or `completed`
- `priority` - integer from 1 through 5; defaults to `1`

Updates are partial: fields omitted from `PUT /tasks/{id}` keep their existing values.
Invalid request bodies return `422`, missing tasks return `404`, successful creation returns `201`, and successful deletion returns `204`.

Tasks are stored in memory and are lost when the server restarts.
