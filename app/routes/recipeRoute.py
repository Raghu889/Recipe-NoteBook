from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import SessionLocal
from schemas import user as user_schema
from schemas import rating as rating_schema
from schemas import save as save_schema
from models.user import User
from models.recipe import Recipe
from models.rating import Rating
from models.save import Save
from utils import hash_password, verify_password, create_access_token, get_current_user
from schemas import recipe
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

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
    recipe_out_list=[]
    for recipe_obj in recipes:
        avg_rating=db.query(func.avg(Rating.rating))\
                     .filter(Rating.recipe_id==recipe_obj.id).scalar()
        
        recipe_data = jsonable_encoder(recipe_obj)
        recipe_data['average_rating']=round(avg_rating, 2) if avg_rating else None

        recipe_out_list.append(recipe.RecipeOut(**recipe_data))
    return recipe_out_list

@router.get("/{recipe_id}",response_model=recipe.RecipeOut)
async def get_recipe_by_id(recipe_id:int,db:Session=Depends(get_db)):
    reci=db.query(Recipe).filter(Recipe.id== recipe_id).first()
    if not reci:
        raise HTTPException(status_code=404,detail="Recipe Not Foud")
    # ✅ Calculate average rating
    avg_rating = db.query(func.avg(Rating.rating))\
                   .filter(Rating.recipe_id == recipe_id)\
                   .scalar()

    recipe_data = jsonable_encoder(reci)
    recipe_data['average_rating'] = round(avg_rating, 2) if avg_rating else None
    return recipe.RecipeOut(**recipe_data)


@router.put("/{recipe_id}",response_model=recipe.RecipeOut)
async def update_recipe(recipe_id:int, updated_data:recipe.RecipeUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
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

@router.post("/{id}/rate", response_model=rating_schema.RateingOut)
async def save_recipe(id:int,rate:rating_schema.RateingIn,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    reci=db.query(Recipe).filter(Recipe.id==id).first()
    if not reci:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if current_user.id==reci.author_id:
        raise HTTPException(status_code=403,detail="Can't Rate the Recipe")
    
     # ✅ Check if user already rated this recipe
    existing_rating = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.recipe_id == id
    ).first()

    if existing_rating:
        raise HTTPException(status_code=400, detail="You have already rated this recipe")
    

    db_rating=Rating(
        user_id=current_user.id,
        recipe_id=id,
        rating=rate.rate,
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating



@router.get("/user/save",response_model=List[recipe.RecipeOut])
def get_saved_recipes(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    user_saves=db.query(Save).filter(Save.user_id==current_user.id).all()
    recipes=[]
    for save in user_saves:
        recipes.append(db.query(Recipe).filter(save.recipe_id==Recipe.id).first())
    return recipes


@router.post("/{id}/save", response_model=save_schema.Save)
async def save_recipe(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    # ❗ Check if already saved
    reci=db.query(Recipe).filter(Recipe.id==id).first()
    if reci.author_id==current_user.id:
        raise HTTPException(status_code=403,detail="Can't save your own recipe")
    existing_save = db.query(Save).filter(
        Save.user_id == current_user.id,
        Save.recipe_id == id
    ).first()

    if existing_save:
        raise HTTPException(status_code=400, detail="You have already saved this recipe.")

    save=Save(
        user_id=current_user.id,
        recipe_id=id
    )

    db.add(save)
    db.commit()
    db.refresh(save)

    return save

@router.delete("/{id}/unsave")
def unsave_recipe(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    # ✅ Check if the recipe is saved by the user
    save_entry = db.query(Save).filter(
        Save.user_id == current_user.id,
        Save.recipe_id == id
    ).first()
    if not save_entry:
        raise HTTPException(status_code=404, detail="Recipe not found in your saved list.")
    # ❌ Delete the save entry
    db.delete(save_entry)
    db.commit()

    return {"detail": "Recipe unsaved successfully."}



@router.get("/user/search", response_model=List[recipe.RecipeOut])
def search_recipes(
    name:Optional[str]=Query(None),
    ingredients:Optional[str]=Query(None),
    db:Session=Depends(get_db)
):
    query=db.query(Recipe)

    if name:
        query = query.filter(Recipe.title.ilike(f"%{name}%"))

    if ingredients:
        ingredients_list=[ing.strip().lower() for ing in ingredients.split(",")]
        for ing in ingredients_list:
            query= query.filter(Recipe.ingredients.ilike(f"%{ing}%"))
    
    results=query.all()

    return results
    