from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class SkinType(Base):
    __tablename__ = "skin_types"

    id = Column(Integer, primary_key=True, index=True)
    skin_type_name = Column(String, nullable=False)
    # translations = relationship("SkinTypeTranslation", back_populates="skin_type", cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "skin_type_name": self.skin_type_name,
        }

    @classmethod
    async def find_by_skintype_id(cls, skintype_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(skintype_id=skintype_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find skintypetranslations: {e}")

    @classmethod
    async def find_all(cls, db: AsyncSession):
        try:
            result = await db.execute(select(cls))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to get all skintypetranslations: {e}")

    async def save_to_db(self, db: AsyncSession):
        try:
            db.add(self)
            await db.commit()
            await db.refresh(self)
            return self
        except SQLAlchemyError as e:
            raise ValueError(f"Error to save skintype translation: {e}")

    async def delete_from_db(self, db: AsyncSession):
        try:
            await db.delete(self)
            await db.commit()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to delete skintype translation: {e}")
