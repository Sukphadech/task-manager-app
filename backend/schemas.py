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

# Schema สำหรับสร้าง Board (ไม่ต้องใส่ id)
class BoardCreate(BaseModel):
    title: str
    owner_id: int

# Schema สำหรับ Response (มี id)
class BoardResponse(BaseModel):
    id: int
    title: str
    owner_id: int

    class Config:
        class Config:
            from_attributes = True
