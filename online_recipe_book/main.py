from fastapi import FastAPI
from online_recipe_book.routers import categories, recipes

app = FastAPI()

app.include_router(categories.router)
app.include_router(recipes.router)