from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

from db import Base

product_ingredient_association = Table(
    "product_ingredient_association",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True)
)
product_category_association = Table(
    "product_category_association",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
)
