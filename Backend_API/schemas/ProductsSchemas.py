from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ========================
# PRODUCTS
# ========================
class ProductCreate(BaseModel):
    product_name: str
    barcode: Optional[str] = None
    brand: Optional[str] = None
    image_url: Optional[str] = None
    ingredients_text: Optional[str] = None
    source: Optional[str] = "obf"
    ingredients: List[int] = []
    categories: List[int] = []

class ProductResponse(BaseModel):
    id: int
    product_name: str
    barcode: Optional[str]
    brand: Optional[str]
    image_url: Optional[str]
    ingredients_text: Optional[str]
    source: str
    created_at: datetime
    ingredients: List[dict] = []
    categories: List[dict] = []
    class Config:
        from_attributes = True
