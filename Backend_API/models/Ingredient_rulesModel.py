from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class IngredientRuleModel(Base):
    __tablename__ = "ingredient_rules"
    id = Column(Integer, primary_key=True, index=True)
    ingredient_a_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    ingredient_b_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    rule_type = Column(String)
    description = Column(Text)
  
    def json(self):
        return {
            "id": self.id,
            "ingredient_a_id": self.ingredient_a_id,
            "ingredient_b_id": self.ingredient_b_id,
            "rule_type": self.rule_type,
            "description": self.description
        }

    @classmethod
    async def find_by_ingredient_id(cls, ingredient_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(ingredient_id=ingredient_id))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find ingredient rules: {e}")