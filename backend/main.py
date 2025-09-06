from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal



# สร้างตารางอัตโนมัติ
models.Base.metadata.create_all(bind=engine)


app = FastAPI()



# Dependency → ใช้ session ต่อกับ DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Models (Pydantic)
# -----------------------------
class User(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class Board(BaseModel):
    id: int
    title: str
    owner_id: int

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    board_id: int

# -----------------------------
# Mock Database (ชั่วคราว)
# -----------------------------
users = []
boards = []
tasks = []

# -----------------------------
# Routes
# -----------------------------
@app.post("/register", response_model=User)
def register(user: UserCreate):
    new_user = User(id=len(users)+1, username=user.username, email=user.email)
    users.append(new_user)
    return new_user

@app.get("/boards", response_model=List[Board])
def get_boards():
    return boards

@app.get("/boards/{board_id}/tasks", response_model=List[Task])
def get_tasks(board_id: int):
    return [task for task in tasks if task.board_id == board_id]

@app.post("/boards", response_model=Board)
def create_board(board: Board):
    boards.append(board)
    return board
@app.post("/boards/{board_id}/tasks", response_model=Task)
def create_task(board_id: int, task: Task):
    task.board_id = board_id
    tasks.append(task)
    return task


@app.get("/boards/{board_id}/tasks", response_model=List[Task])
def get_tasks(board_id: int):
    return [task for task in tasks if task.board_id == board_id]


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": f"Task {task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/boards/{board_id}", response_model=Board)
def update_board(board_id: int, updated_board: Board):
    for i, board in enumerate(boards):
        if board.id == board_id:
            boards[i] = updated_board
            return updated_board
    raise HTTPException(status_code=404, detail="Board not found")

@app.delete("/boards/{board_id}")
def delete_board(board_id: int):
    for i, board in enumerate(boards):
        if board.id == board_id:
            boards.pop(i)
            return {"message": f"Board {board_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Board not found")