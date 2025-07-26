from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class UserHistoryModel(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("UsersModel", back_populates="history")
    product = relationship("ProductModel")

    def json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "timestamp": self.timestamp 
        }

    @classmethod
    async def find_by_user_id(cls, user_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(user_id=user_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find user history by user ID: {e}")