from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# INGREDIENTS
# ========================
class IngredientCreate(BaseModel):
    ingredient_name: str
    description: Optional[str] = None
    ai_generated: Optional[bool] = False
    function: Optional[str] = None
    products: List[int] = []

class IngredientResponse(BaseModel):
    id: int
    ingredient_name: str
    description: Optional[str]
    ai_generated: bool
    products: List[dict] = []
    class Config:
        orm_mode = True
