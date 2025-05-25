from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from dotenv import load_dotenv

from db import get_db, Base, engine
from resources import router as router_products

load_dotenv()
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
)

@app.on_event("startup")
async def startup_event():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

@app.get("/check_connection")
async def check_connection(db: AsyncSession = Depends(get_db)):
  try:
    return {"status": "Backend is connected to the frontend"}
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
app.include_router(router_products, prefix="/products")
  
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)