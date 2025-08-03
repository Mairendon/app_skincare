from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# ROUTINES
# ========================
class RoutineStepResponse(BaseModel):
    id: int
    routine_id: int
    product_id: int
    step_order: int
    class Config:
        from_attributes = True

class RoutineResponse(BaseModel):
    id: int
    user_id: int
    routine_name: str
    steps: List[RoutineStepResponse] = []
    class Config:
        from_attributes = True

class RoutineCreate(BaseModel):
    user_id: int
    routine_name: str
    steps: List[dict] = []