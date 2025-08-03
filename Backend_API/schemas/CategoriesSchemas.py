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
        from_attributes = True

class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    class Config:
        from_attributes = True
