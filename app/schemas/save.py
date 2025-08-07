from pydantic import BaseModel
from typing import List, Optional


class Save(BaseModel):
    id:int
    user_id:int
    recipe_id: int