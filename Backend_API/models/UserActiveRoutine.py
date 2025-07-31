from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class UserActiveRoutine(Base):
    __tablename__ = "user_active_routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    routine_id = Column(Integer, ForeignKey("routines.id", ondelete="CASCADE"))
    routine_type = Column(String, nullable=False)

    user = relationship("UsersModel", back_populates="active_routines")
    routine = relationship("Routine", back_populates="active_users")

    __table_args__ = (
        UniqueConstraint("user_id", "routine_type", name="unique_user_routine_type"),
    )
