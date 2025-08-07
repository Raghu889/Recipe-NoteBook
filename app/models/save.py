from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Save(Base):
    __tablename__="saves"

    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    recipe_id=Column(Integer,ForeignKey("recipes.id"))
    
    user=relationship("User",back_populates="saves")
    recipe=relationship("Recipe",back_populates="save")

    