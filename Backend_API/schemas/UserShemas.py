from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.RoutinesSchemas import RoutineResponse, RoutineStepResponse
from schemas.ProductsSchemas import ProductResponse
# ========================
# AUTH / TOKENS
# ========================
class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ========================
# USERS
# ========================
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

# Active Routine (moved up because UserResponse depends on it)
class UserActiveRoutineResponse(BaseModel):
    id: int
    user_id: int
    routine_id: int
    routine_type: str
    class Config:
        orm_mode = True

class UserActiveRoutineCreate(BaseModel):
    user_id: int
    routine_id: int
    routine_type: str

# History (before UserResponse)
class UserHistoryResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    class Config:
        orm_mode = True

# UserResponse (final step after all components defined)
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    history: List[UserHistoryResponse] = []
    routines: List[RoutineResponse] = []
    active_routine: Optional[UserActiveRoutineResponse] = None
    class Config:
        orm_mode = True
