from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    ingredients = Column(String(1000), nullable=False)  # Comma-separated
    instructions = Column(String(5000), nullable=False)
    simplified_instructions = Column(String(5000))
    calories = Column(Integer)
    tags = Column(String(225))
    author_id = Column(Integer, ForeignKey("users.id"))
    average_rating=Column(Float,default=0.0)
    no_of_ratings=Column(Integer,default=0)

    author = relationship("User", back_populates="recipes")
    ratings=relationship("Rating",back_populates="recipe")
    save=relationship("Save",back_populates="recipe")




