from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/user_login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    user_id = int(payload.get("sub"))

    result = await db.execute(
        select(UsersModel)
        .options(
            selectinload(UsersModel.history),
            selectinload(UsersModel.routines),
            selectinload(UsersModel.active_routines)
        )
        .where(UsersModel.id == user_id)
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
