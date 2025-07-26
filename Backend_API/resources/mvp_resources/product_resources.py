from fastapi import APIRouter, HTTPException, Depends, status, Path
from pydantic import BaseModel, Field

from typing import List
from db import get_db
from models.ProductsModel import ProductModel

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

router = APIRouter()

@router.get("/products")
async def get_all_products():
    p = await ProductModel.find_all()
    if not p:
        raise HTTPException(status_code=404, detail="No products found")
    return [
        {
            "id": p.id,
            "product_name": p.product_name,
            "barcode": p.barcode,
            "categories": p.categories,
            "ingredients_text": p.ingredients_text,
            "source": p.source,
            "created_at": p.created_at
        }
    ]