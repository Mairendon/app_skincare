from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class CategoryTranslation(Base):
    __tablename__ = "category_translations"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    language = Column(String, nullable=False)
    translated_name = Column(String, nullable=False)

    # category = relationship("Category", back_populates="translations")

    def json(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "language": self.language,
            # "translated_name": self.translated_name
        }

    @classmethod
    async def find_by_category_id(cls, category_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(category_id=category_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find category translations: {e}")

    @classmethod
    async def find_all(cls, db: AsyncSession):
        try:
            result = await db.execute(select(cls))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to get all category translations: {e}")

    async def save_to_db(self, db: AsyncSession):
        try:
            db.add(self)
            await db.commit()
            await db.refresh(self)
            return self
        except SQLAlchemyError as e:
            raise ValueError(f"Error to save category translation: {e}")

    async def delete_from_db(self, db: AsyncSession):
        try:
            await db.delete(self)
            await db.commit()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to delete category translation: {e}")
