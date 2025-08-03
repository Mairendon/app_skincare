from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# INGREDIENT RULES
# ========================
class IngredientRuleCreate(BaseModel):
    ingredient_a_id: int
    ingredient_b_id: int
    rule_type: str
    description: Optional[str] = None

class IngredientRuleResponse(BaseModel):
    id: int
    ingredient_a_id: int
    ingredient_b_id: int
    rule_type: str
    description: Optional[str] = None
    class Config:
        from_attributes = True
