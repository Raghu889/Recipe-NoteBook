from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas import user as user_schema
from models.user import User
from models.recipe import Recipe
from utils import hash_password, verify_password, create_access_token, get_current_user
from schemas import recipe
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=recipe.RecipeOut)
def create_recipe(recipe:recipe.RecipeUpdate, db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    db_recipe=Recipe(
        title=recipe.title,
        ingredients=",".join(recipe.ingredients),
        instructions=recipe.instructions,
        tags=",".join(recipe.tags),
        author_id=current_user.id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


@router.get("/",response_model=List[recipe.RecipeOut])
async def get_recipes(db:Session=Depends(get_db)):
    recipes= db.query(Recipe).all()
    
    return recipes

@router.get("/{recipe_id}",response_model=recipe.RecipeOut)
async def get_recipe_by_id(recipe_id:int,db:Session=Depends(get_db)):
    reci=db.query(Recipe).filter(Recipe.id== recipe_id).first()
    if not reci:
        raise HTTPException(status_code=404,detail="Recipe Not Foud")
    return reci


@router.put("/{recipe_id}",response_model=recipe.RecipeOut)
async def update_recipe(recipe_id:int, updated_data:recipe.RecipeCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    reci=db.query(Recipe).filter(Recipe.id==recipe_id).first();

    if not reci:
        raise HTTPException(status_code=404,detail="Recipe Not Foud")

    if reci.author_id!=current_user.id:
        raise HTTPException(status_code=403,detail="You Are Not Authorized To Edit This Recipe")


    for field,value in updated_data.dict(exclude_unset=True).items():
        if isinstance(value, list):
            value = ",".join(value)
        setattr(reci,field,value)

    db.commit()
    db.refresh(reci)
    return reci     

@router.delete("/{recipe_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    reci=db.query(Recipe).filter(Recipe.id==recipe_id).first()
    if not reci:
        raise HTTPException(status_code=404,detail="Recipe Not Found")
    
    if reci.author_id!=current_user.id:
        raise HTTPException(status_code=403,detail="You Have No Permission To Delete This Recipe")
    
    db.delete(reci)
    db.commit()
    return None