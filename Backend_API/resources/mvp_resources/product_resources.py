from fastapi import APIRouter, HTTPException, Depends, status, Path
from pydantic import BaseModel, Field

from typing import List
from db import get_db
from models.ProductsModel import ProductModel
from schemas.ProductsSchemas import ProductCreate, ProductResponse, ProductListResponse

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/products")
async def get_all_products(db: AsyncSession = Depends(get_db)):
    p = await ProductModel.find_all(db)
    if not p:
        raise HTTPException(status_code=404, detail="No products found")
    return ProductListResponse(
        products=[
            ProductResponse.model_validate(prod, from_attributes=True)
            for prod in p
        ]
    )

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        
        new_product = ProductModel(
            product_name=product.product_name,
            barcode=product.barcode,
            brand=product.brand,
            image_url=product.image_url,
            ingredients_text=product.ingredients_text,
            source=product.source
        )

        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)

        return {
            "id": new_product.id,
            "product_name": new_product.product_name,
            "barcode": new_product.barcode,
            "brand": new_product.brand,
            "image_url": new_product.image_url,
            "ingredients_text": new_product.ingredients_text,
            "source": new_product.source,
            "created_at": new_product.created_at
        }
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=400, detail=str(e))
