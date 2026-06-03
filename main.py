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
                priority VARCHAR(4)
            )
        ''')
        conn.commit()
    yield

app = FastAPI(lifespan=data_base)

class PriorityLevels(str, Enum):
    LOW = 'Low'
    MID = 'Mid'
    HIGH = 'High'

class Task(BaseModel):
    key: str
    title: str
    description: str | None = None
    priority: PriorityLevels

    @field_validator('key')
    @classmethod
    def validate_key(cls, value: str) -> str:
        if len(value) != 4 or not value.isdigit():
            raise ValueError("Key must be 4 digits")
        return value

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
        INSERT INTO tasks (key, title, description, priority)
            VALUES (?, ?, ?, ?)
        ''', (task.key, task.title, task.description, task.priority.value))
    conn.commit()
    conn.close()
    return {
        "status": "Task created",
        "data": {
            "key": task.key,
            "title": task.title,
            "description": task.description,
            "difficulty": task.priority,
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