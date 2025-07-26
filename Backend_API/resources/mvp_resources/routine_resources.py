from fastapi import APIRouter, HTTPException, Depends, status, Path
from pydantic import BaseModel, Field

from typing import List
from db import get_db
from models import RoutinesModel

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

router = APIRouter()