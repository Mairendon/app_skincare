from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================
# USERS
# ========================
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserHistoryResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    class Config:
        orm_mode = True

class RoutineStepResponse(BaseModel):
    id: int
    routine_id: int
    product_id: int
    step_order: int
    class Config:
        orm_mode = True

class RoutineResponse(BaseModel):
    id: int
    user_id: int
    routine_name: str
    steps: List[RoutineStepResponse] = []
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    history: List[UserHistoryResponse] = []
    routines: List[RoutineResponse] = []
    class Config:
        orm_mode = True

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
        orm_mode = True

# ========================
# ROUTINES
# ========================
class RoutineCreate(BaseModel):
    user_id: int
    routine_name: str
    steps: List[dict] = []

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
        orm_mode = True
