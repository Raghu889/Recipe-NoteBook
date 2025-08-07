from pydantic import BaseModel
from typing import List, Optional

class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    tags: Optional[List[str]] = []

class RecipeOut(BaseModel):
    id: int
    title: str
    ingredients: str
    instructions: str
    simplified_instructions: Optional[str]
    calories: Optional[int]
    tags: str
    author_id: int
    average_rating:Optional[float]=None

    class Config:
        orm_mode = True


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[str] = None
    tags: Optional[List[str]] = None