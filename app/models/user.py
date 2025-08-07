from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    recipes = relationship("Recipe", back_populates="author")
    ratings = relationship("Rating", back_populates="rater")
    saves=relationship("Save",back_populates="user")
    
