from fastapi import FastAPI
from online_recipe_book.routers import categories

app = FastAPI()

app.include_router(categories.router)