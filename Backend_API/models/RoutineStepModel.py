from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base

class RoutineStep(Base):
    __tablename__ = "routine_steps"
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    step_order = Column(Integer, nullable=False)

    routine = relationship("Routine", back_populates="steps")
    product = relationship("ProductModel")

    def json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "step_order": self.step_order
        }

    @classmethod
    async def find_by_routine_id(cls, routine_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(routine_id=routine_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find routine steps by routine ID: {e}")