from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from resources.categorize_product import order_products_by_routine
import httpx
router = APIRouter()

class ProductInput(BaseModel):
  product_name: Optional[str]
  categories: Optional[str]
  ingredients_text: Optional[str] = ""

@router.post("/routine")
async def generate_routine(products: List[ProductInput]):
  product_dicts = [product.dict() for product in products]
  ordered = order_products_by_routine(product_dicts)

  if not ordered:
    raise HTTPException(status_code=400, detail="No valid routine steps founds.")
  
  return{"routine": ordered}

class ProductNameOnly(BaseModel):
    product_name: str

@router.post("/products/generate_full_routine")
async def generate_full_routine(products: List[ProductNameOnly]):
    enriched_products = []
    async with httpx.AsyncClient() as client:
        for p in products:
            search_url = "https://world.openbeautyfacts.org/cgi/search.pl"
            params = {
                "search_terms": p.product_name,
                "search_simple": 1,
                "action": "process",
                "json": 1
            }
            response = await client.get(search_url, params=params)
            
            if response.status_code != 200:
                continue

            product_list = response.json().get("products", [])
            if not product_list:
                continue

            product_data = product_list[0]  # usar el primer resultado válido

            enriched_products.append({
                "product_name": product_data.get("product_name", p.product_name),
                "categories": product_data.get("categories", ""),
                "ingredients_text": product_data.get("ingredients_text", "")
            })

    if not enriched_products:
        raise HTTPException(status_code=404, detail="No valid product data found from Open Beauty Facts.")

    routine = order_products_by_routine(enriched_products)
    if not routine:
        raise HTTPException(status_code=400, detail="Could not determine routine steps.")

    return {"routine": routine}
