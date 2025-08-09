from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(225))

    recipes = relationship("Recipe", back_populates="author")
    ratings = relationship("Rating", back_populates="rater")
    saves=relationship("Save",back_populates="user")

