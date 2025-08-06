from fastapi import FastAPI
from routes import recipeRoute
from routes import auth
from db import engine
from models import user,recipe



user.Base.metadata.create_all(bind=engine)
recipe.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(recipeRoute.router, prefix="/api/recipe", tags=["Recipe"])