from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from db import get_db
from models.UsersModel import UsersModel
from resources.Auth.Auth import (
    decode_token, verify_password, 
    SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINS, ALGORITHM
    )
from resources.mvp_resources.users_resources import get_current_user
from schemas.UserShemas import UserResponse

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UsersModel).where(UsersModel.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.get("/me", response_model=UserResponse)
async def get_user_me(current_user: UsersModel = Depends(get_current_user)):
    return current_user


