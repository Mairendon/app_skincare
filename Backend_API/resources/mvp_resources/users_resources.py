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
from schemas.UserShemas import (
    UserCreate, UserResponse, UserHistoryResponse, 
    RoutineResponse, RoutineStepResponse, UserLogin
    )

router = APIRouter()

oath2_scheme = OAuth2PasswordBearer(tokenUrl="users/user_login")

async def get_current_user(token: str = Depends(oath2_scheme), db: AsyncSession = Depends(get_db)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    user_id = int(payload.get("sub"))
    result = await db.execute(select(UsersModel).where(UsersModel.id == user_id))
    user = result.scalar().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


