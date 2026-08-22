import sqlite3
from contextlib import asynccontextmanager
from enum import Enum

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, field_validator

@asynccontextmanager
async def data_base(_: FastAPI):
    with sqlite3.connect("task_manager.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks(
                key VARCHAR(4) PRIMARY KEY,
                title VARCHAR(30),
                description VARCHAR(100),
                priority VARCHAR(4),
                status VARCHAR(11),
                assigned VARCHAR(30)
            )
        ''')
        conn.commit()
    yield

app = FastAPI(lifespan=data_base)

class PriorityLevels(str, Enum):
    LOW = 'Low'
    MID = 'Mid'
    HIGH = 'High'

class StatusLevels(str, Enum):
    NEW = 'New'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'

class Task(BaseModel):
    key: str
    title: str
    description: str | None = None
    priority: PriorityLevels
    status: StatusLevels = StatusLevels.NEW
    assigned: str | None = None

    @field_validator('key')
    @classmethod
    def validate_key(cls, value: str) -> str:
        if len(value) != 4 or not value.isdigit():
            raise ValueError("Key must be 4 digits")
        return value

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityLevels
    status: StatusLevels
    assigned: str | None = None

@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return {"Tasks": tasks}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(task: Task):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (key, title, description, priority, status, assigned)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task.key, task.title, task.description, task.priority.value, task.status.value, task.assigned))
    conn.commit()
    conn.close()
    return {
        "status": "Task created",
        "data": {
            "key": task.key,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "assigned": task.assigned,
        }
    }


@app.delete("/tasks/{task_key}")
def delete_task(task_key: str):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM tasks WHERE key=?", (task_key,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with key {task_key} not found"
        )
    cursor.execute('''DELETE
                      FROM tasks
                      WHERE key =?''', (task_key,))
    conn.commit()
    conn.close()
    return {"status": f"Successfully deleted task with key: {task_key}"}

@app.get("/tasks/{task_key}")
def get_task_by_key(task_key: str):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE key=?", (task_key,))
    task = cursor.fetchone()
    conn.close()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with key {task_key} not found"
        )
    return {"Task": task}

@app.put("/tasks/{task_key}", status_code=status.HTTP_200_OK)
def update_task(task_key: str, task_data: TaskUpdate):
    conn = sqlite3.connect("task_manager.db")
    cursor = conn.cursor()

    cursor.execute("SELECT key FROM tasks WHERE key = ?", (task_key,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with key {task_key} not found"
        )

    cursor.execute('''
        UPDATE tasks 
        SET title = ?, description = ?, priority = ?, status = ?, assigned = ?
        WHERE key = ?
    ''', (
        task_data.title,
        task_data.description,
        task_data.priority.value,
        task_data.status.value,
        task_data.assigned,
        task_key
    ))

    conn.commit()
    conn.close()

    return {
        "status": f"Task {task_key} updated",
        "data": {
            "key": task_key,
            "title": task_data.title,
            "description": task_data.description,
            "priority": task_data.priority,
            "status": task_data.status,
            "assigned": task_data.assigned,
        }
    }
