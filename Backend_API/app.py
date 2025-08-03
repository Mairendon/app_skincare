from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from dotenv import load_dotenv

from db import get_db, Base, engine
# from resources import router as router_products
# from router.routine import router as router_routine

from resources.mvp_resources.ingredients_resources import router as router_ingredients
from resources.mvp_resources.product_resources import router as router_products
from resources.mvp_resources.routine_resources import router as router_routines
from resources.mvp_resources.categories_resources import router as router_categories
from resources.mvp_resources.routine_steps_resources import router as router_routine_steps
from resources.mvp_resources.user_history_resources import router as router_user_history
from resources.mvp_resources.active_routine_resources import router as router_active_routine
from router.user_router import router as router_users
from resources.Auth.Auth import router as auth_router

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
  
app.include_router(auth_router, prefix="/auth")
app.include_router(router_products, prefix="/products")
# app.include_router(router_routine, prefix="/routine")
app.include_router(router_ingredients, prefix="/ingredients")
app.include_router(router_routines, prefix="/routines")
app.include_router(router_categories, prefix="/categories")
app.include_router(router_user_history, prefix="/user_history")
app.include_router(router_routine_steps, prefix="/routine_steps")
app.include_router(router_active_routine, prefix="/active_routine")
app.include_router(router_users, prefix="/users")
  
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)