from fastapi import APIRouter, HTTPException, Depends, status, Path
from pydantic import BaseModel, Field

from typing import List
from db import get_db
from models.CategoriesModel import Category
from schemas.CategoriesSchemas import CategoryCreate, CategoryListResponse, CategoryResponse

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

router = APIRouter()

@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await Category.find_all(db) 
    return CategoryListResponse(
        categories=[
            CategoryResponse.model_validate(cat, from_attributes=True)
            for cat in categories
        ]
    )
 