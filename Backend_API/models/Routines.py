from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base

class Routine(Base):
  __tablename__ = "routines"
  id = Column(Integer, primary_key=True, index=True)
  routine_name = Column(String, nullable=False)
  step_order = Column(Integer, nullable=False)
  created_at = Column(DateTime, server_default=func.now())

  def json(self):
    return {
        "id": self.id,
        "routine_name": self.routine_name,
        "step_order": self.step_order,
        "created_at": self.created_at
    }

  @classmethod
  async def find_by_routinename(cls, routine_name:str, db: AsyncSession):
    try:
      result = await db.execute(select(cls).filter_by(routine_name=routine_name))
      return result.scalar().first()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to find routine name: {e}")

  @classmethod
  async def find_all(cls, db):
    try:
      result = await db.execute(select(cls).options(joinedload(cls.routines)))
      return result.scalars().all()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to get all routines: {e}")
    
  async def save_to_db(self, db: AsyncSession):
    try:
      db.add(self)
      await db.commit()
      await db.refresh(self)
      return self
    except SQLAlchemyError as e:
      raise ValueError(f"Error to save routine: {e}")
  
  async def delete_from_db(self, db: AsyncSession):
    try:
      await db.delete(self)
      await db.commit()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to delete routine: {e}")
    
  @classmethod
  async def find_by_id(cls, routine_id: int, db: AsyncSession):
    try:
      result = await db.execute(select(cls).filter_by(id=routine_id))
      return result.scalar().first()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to find routine by id:  {e}")