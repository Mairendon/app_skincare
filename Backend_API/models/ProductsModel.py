from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.IngredientsModel import IngredientModel
from models.RelationsTable import product_ingredient_association, product_category_association


from db import Base

def joinedload(*args, **kwargs):
    raise NotImplementedError

class ProductModel(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key=True, index=True)
  product_name = Column(String, nullable=False)
  barcode = Column(String, nullable=False)
  brand = Column(String, nullable=True)
  image_url = Column(Text, nullable=True)
  categories = Column(Text)
  ingredients_text = Column(Text)
  source = Column(String, default="obf" )
  created_at = Column(DateTime, server_default=func.now())

  ingredients = relationship("IngredientModel", secondary=product_ingredient_association, back_populates="products")
  categories = relationship("Category", secondary=product_category_association, back_populates="products")

  def json(self): 
    return {
      "id": self.id,
      "product_name": self.product_name,
      "barcode": self.barcode,
      "categories": self.categories,
      "ingredients_text": self.ingredients_text,
      "source": self.source,
      "created_at": self.created_at,
      "brand": self.brand,
      "image_url": self.image_url
    }
  
  @classmethod
  async def find_by_productname(cls, product_name:str, db: AsyncSession):
    try:
      result = await db.execute(select(cls).filter_by(product_name=product_name))
      return result.scalar().first()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to find product name: {e}")
    
  @classmethod
  async def find_all(cls, db):
    try:
      result = await db.execute(select(cls).options(joinedload(cls.products)))
      return result.scalars().all()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to get all products: {e}")
    
  async def save_to_db(self, db: AsyncSession):
    try:
      db.add(self)
      await db.commit()
      await db.refresh(self)
      return self
    except SQLAlchemyError as e:
      raise ValueError(f"Error to save product: {e}")
  
  async def delete_from_db(self, db: AsyncSession):
    try:
      await db.delete(self)
      await db.commit()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to delete product: {e}")
    
  @classmethod
  async def find_by_id(cls, product_id: int, db: AsyncSession):
    try:
      result = await db.execute(select(cls).filter_by(id=product_id))
      return result.scalar().first()
    except SQLAlchemyError as e:
      raise ValueError(f"Error to find product by id:  {e}")