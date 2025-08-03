from fastapi import APIRouter, HTTPException, Depends, status, Path
from pydantic import BaseModel, Field

from typing import List
from db import get_db
from models.CategoriesModel import Category

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

router = APIRouter()

async def get_categories(db: AsyncSession = Depends(get_db)) -> List[Category]:
    try:
        result = await db.execute(select(Category).options(joinedload(Category.parent_category)))
        categories = result.scalars().all()
        return categories
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))