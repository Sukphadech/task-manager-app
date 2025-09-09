from pydantic import BaseModel
from typing import Optional



# -------------------------
# Task Schemas
# -------------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    board_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    board_id: int

    class Config:
        from_attributes = True   

# -------------------------
# Board Schemas
# -------------------------
class BoardCreate(BaseModel):
    title: str


class BoardResponse(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        class Config:
            from_attributes = True

# -------------------------
# User Schemas
# -------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
 
class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

