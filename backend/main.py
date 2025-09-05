from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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
