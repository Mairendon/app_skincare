from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from db import Base

class UsersModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    active_routine = relationship("UserActiveRoutine", back_populates="user", cascade="all, delete-orphan")
    history = relationship("UserHistoryModel", back_populates="user", cascade="all, delete-orphan")
    routines = relationship("Routine", back_populates="user", cascade="all, delete-orphan")

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "history": [h.json() for h in self.history],
            "routines": [routine.json() for routine in self.routines]
            # "is_active": self.is_active
        }

    @classmethod
    async def find_by_email(cls, email: str, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(email=email))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find user by email: {e}")

    @classmethod
    async def find_all(cls, db: AsyncSession):
        try:
            result = await db.execute(select(cls))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to get all users: {e}")

    async def save_to_db(self, db: AsyncSession):
        try:
            db.add(self)
            await db.commit()
            await db.refresh(self)
            return self
        except SQLAlchemyError as e:
            raise ValueError(f"Error to save user: {e}")

    async def delete_from_db(self, db: AsyncSession):
        try:
            await db.delete(self)
            await db.commit()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to delete user: {e}")

    @classmethod
    async def find_by_id(cls, user_id: int, db: AsyncSession):
        try:
            result = await db.execute(select(cls).filter_by(id=user_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise ValueError(f"Error to find user by id: {e}")
