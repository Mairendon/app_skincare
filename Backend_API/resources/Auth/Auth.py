from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from db import get_db
from models.UsersModel import UsersModel
from schemas.UserShemas import (
    UserCreate,
    UserLogin,
    TokenResponse
    )

from jose import jwt, JWSError
from passlib.context import CryptContext

from dotenv import load_dotenv
from datetime import timedelta, datetime
import os
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINS", 30))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(pasword: str) -> str:
    return pwd_context.hash(pasword)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWSError:
        return None

@router.post("/", response_model=TokenResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UsersModel).where(UsersModel.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)

    new_user = UsersModel(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer" }

@router.post("/user_login", response_model=TokenResponse)
async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UsersModel).where(UsersModel.email == user.email))
    existing_user = result.scalars().first()

    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(existing_user.id)})
    return {"access_token": token, "token_type": "bearer"}
