from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List
from datetime import datetime
import unicodedata

def _to_inci(s: str) -> str:
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s

# ========================
# INGREDIENTS
# ========================
class IngredientCreate(BaseModel):
    ingredient_name: str
    description: Optional[str] = None
    ai_generated: Optional[bool] = False
    function: Optional[str] = None
    products: List[int] = Field(default_factory=list)

    @field_validator('ingredient_name')
    @classmethod
    def normalize_inci(cls, v: str) -> str:
        return _to_inci(v)
    
class IngredientResponse(BaseModel):
    id: int
    ingredient_name: str
    description: Optional[str]
    ai_generated: bool
    function: Optional[str] = None
    products: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True

class IngredientAliasCreate(BaseModel):
    ingredient_id: int
    alias: str

    @field_validator("alias")
    @classmethod
    def normalize_alias(cls, v: str) -> str:
        return _to_inci(v)

class IngredientAliasResponse(BaseModel):
    id: int
    ingredient_id: int
    alias: str

    class Config:
        from_attributes = True