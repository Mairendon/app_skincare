from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.RelationsTable import product_category_association

from db import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)

    products = relationship("ProductModel", secondary=product_category_association, back_populates="categories")

    # translations = relationship("CategoryTranslation", back_populates="category", cascade="all, delete-orphan")

    # url = Column(String, nullable=False)
    # parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # # Relación para subcategorías
    # subcategories = relationship("Category", backref="parent", remote_side=[id])

    def json(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            # "url": self.url,
            # "parent_id": self.parent_id
        }

    @classmethod
    async def find_by_categoryname(cls, category_name: str, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(category_name=category_name))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find category name: {e}")

    @classmethod
    async def find_all(cls, db: AsyncSession):
        try:
            result = await db.execute(select(cls))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to get all categories: {e}")

    async def save_to_db(self, db: AsyncSession):
        try:
            db.add(self)
            await db.commit()
            await db.refresh(self)
            return self
        except SQLAlchemyError as e:
            raise ValueError(f"Error to save category: {e}")

    async def delete_from_db(self, db: AsyncSession):
        try:
            await db.delete(self)
            await db.commit()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to delete category: {e}")

    @classmethod
    async def find_by_id(cls, category_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(id=category_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find category by id: {e}")
