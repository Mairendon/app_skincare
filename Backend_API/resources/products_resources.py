import httpx
import logging
from fastapi import APIRouter, HTTPException

from models.ProductsModel import Product

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/search_by_name")
async def search_by_name(product_name: str):
    search_url = "https://world.openbeautyfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Search request failed")

    results = response.json().get("products", [])
    return {"results": results[:5]}  # Devuelve los primeros 5 resultados

