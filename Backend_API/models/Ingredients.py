from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, func
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base

class Ingredient(Base):
  __tablename__ = "ingredients"

  id = Column(Integer, primary_key=True, index=True)
  Ingredient_name = Column(String, nullable=False)
  description = Column(Text)
  created_at = Column(DateTime, server_default=func.now())
  ai_generated = Column(Boolean, default=False)

  def json(self):
    return {
        "id": self.id,
        "Ingredient_name": self.Ingredient_name,
        "description": self.description,
        "created_at": self.created_at
    }

  @classmethod
  async def find_by_ingredientname(cls, ingredient_name: str, db: AsyncSession):
    try:
        result = await db.execute(select(cls).filter_by(Ingredient_name=ingredient_name))
        return result.scalar().first()
    except SQLAlchemyError as e:
        raise ValueError(f"Error to find ingredient name: {e}")
    
  @classmethod
  async def find_all(cls, db):
    try:
      result = await db.execute(select(cls).options(joinedload(cls.ingredients)))
      return result.scalars().all()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to get all ingredients: {e}")
    
  async def save_to_db(self, db: AsyncSession):
    try:
      db.add(self)
      await db.commit()
      await db.refresh(self)
      return self
    except SQLAlchemyError as e:
      raise ValueError(f"Error to save ingredient: {e}")
  
  async def delete_from_db(self, db: AsyncSession):
    try:
      await db.delete(self)
      await db.commit()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to delete ingredient: {e}")
    
  @classmethod
  async def find_by_id(cls, ingredient_id: int, db: AsyncSession):
    try:
      result = await db.execute(select(cls).filter_by(id=ingredient_id))
      return result.scalar().first()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to find ingredient by id:  {e}")