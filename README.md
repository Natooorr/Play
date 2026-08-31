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

Start the API with:

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`.

## Running tests

```bash
pytest tests/
```
