from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
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
    source: Literal["obf", "manual", "import"] = "obf"
    ingredients: List[int] = Field(default_factory=list)
    categories: List[int] = Field(default_factory=list)

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

class ProductIngredientCreate(BaseModel):
    product_id: int
    ingredient_id: int
    position: int

class ProductIngredientInResponse(BaseModel):
    ingredient_id: int
    position: int

class ProductResponse(BaseModel):
    id: int
    product_name: str
    barcode: Optional[str]
    brand: Optional[str]
    image_url: Optional[str]
    ingredients_text: Optional[str]
    source: str
    created_at: datetime
    
    ingredients: List[ProductIngredientInResponse] = Field(default_factory=list)
    categories: List[dict] = Field(default_factory=list)
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    products: List[ProductResponse]