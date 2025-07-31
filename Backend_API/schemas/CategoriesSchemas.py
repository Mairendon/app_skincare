from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# CATEGORIES
# ========================
class CategoryCreate(BaseModel):
    category_name: str

class CategoryResponse(BaseModel):
    id: int
    category_name: str
    class Config:
        orm_mode = True

class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    class Config:
        orm_mode = True
