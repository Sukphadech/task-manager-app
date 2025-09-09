from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Board
from auth import get_current_user, User
from schemas import BoardCreate, BoardResponse


router = APIRouter(
    prefix="/boards",
    tags=["boards"]
)

@router.post("/")
def create_board(board: BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_board = Board(title=board.title, owner_id=current_user.id)  # 👈 เอา owner_id จาก token
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@router.get("/boards")
def read_boards(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    boards = db.query(Board).filter(Board.owner_id == current_user.id).all()
    return boards



