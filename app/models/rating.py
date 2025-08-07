from sqlalchemy import Column, Integer, String, ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base


class Rating(Base):
    __tablename__ = "ratings"

    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id= Column(Integer, ForeignKey("recipes.id"))
    rating=Column(Integer)

    rater=relationship("User", back_populates="ratings")
    recipe=relationship("Recipe",back_populates="ratings")

