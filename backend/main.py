from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import get_db



SQLALCHEMY_DATABASE_URL = "sqlite:///./taskmanager.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# สร้างตารางอัตโนมัติ
models.Base.metadata.create_all(bind=engine)


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


####################Board#######################
################################################

@app.post("/boards/{board_id}/tasks", response_model=schemas.TaskResponse)
def create_task(board_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        board_id=board_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/boards/{board_id}/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(board_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.board_id == board_id).all()

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.status = updated_task.status
    db_task.board_id = updated_task.board_id
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}


####################Board#######################
################################################
@app.post("/boards", response_model=schemas.BoardResponse)
def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db)):
    db_board = models.Board(title=board.title, owner_id=board.owner_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@app.get("/boards", response_model=list[schemas.BoardResponse])
def get_boards(db: Session = Depends(get_db)):
    return db.query(models.Board).all()


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