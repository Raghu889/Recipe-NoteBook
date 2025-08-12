from fastapi import FastAPI
from app.routes import recipeRoute
from app.routes import auth
from app.db import engine
from app.models import user,recipe,rating, save



user.Base.metadata.create_all(bind=engine)
recipe.Base.metadata.create_all(bind=engine)
rating.Base.metadata.create_all(bind=engine)
save.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(recipeRoute.router, prefix="/api/recipe", tags=["Recipe"])

@app.get("/")
async def root():
    return {"message":"API is runnig"}