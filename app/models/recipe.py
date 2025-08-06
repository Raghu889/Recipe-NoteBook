from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)  # Comma-separated
    instructions = Column(Text, nullable=False)
    simplified_instructions = Column(Text)
    calories = Column(Integer)
    tags = Column(String)
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="recipes")
