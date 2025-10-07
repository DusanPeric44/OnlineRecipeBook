from fastapi import FastAPI
from routers import recipes, categories
import os
from dotenv import load_dotenv
from database import get_db_connection

# Load environment variables from the .env file
load_dotenv()

# Retrieve the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an instance of FastAPI
app = FastAPI()

# Include routers for handling category and recipe-related routes
app.include_router(categories.router)
app.include_router(recipes.router)


@app.on_event("startup")
def startup():
    """
    Event handler for application startup.

    This function is executed when the FastAPI application starts. It establishes
    a connection to the database and creates the necessary tables if they do not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the `categories` table if it does not exist
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS categories (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT UNIQUE NOT NULL
       )
       """)

    # Create the `recipes` table if it does not exist
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS recipes (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           description TEXT,
           ingredients TEXT,
           instructions TEXT,
           cuisine TEXT,
           difficulty TEXT,
           category_id INTEGER,
           FOREIGN KEY (category_id) REFERENCES categories (id)
       )
       """)
    conn.commit()
    conn.close()


@app.get("/")
def read_root():
    """
    Root endpoint for the FastAPI application.

    Returns:
        dict: A dictionary with a welcome message indicating the project.
    """
    return {"message": "FastAPI with SQLite project"}