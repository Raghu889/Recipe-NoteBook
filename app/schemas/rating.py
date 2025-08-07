from pydantic import BaseModel
from typing import List, Optional

class RateingOut(BaseModel):
    id:int
    user_id:int
    recipe_id:int
    rating: int

class RateingIn(BaseModel):
    rate:int