import sqlite3
from streamlit import status
from fastapi import APIRouter, HTTPException
from typing import List
from database import get_db_connection
from models.category import Category, CategoryCreate

router = APIRouter()
routerName = "/categories/"

# Vraca sve kategorije iz baze podataka
@router.get(f"{routerName}", response_model=List[Category])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()

    category_list = [{"id": cat[0], "name": cat[1]} for cat in categories]
    return category_list

# Kreiranje kategorije
@router.post(f"{routerName}", response_model=Category)
def create_category(category: CategoryCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
        conn.commit()
        category_id = cursor.lastrowid
        return Category(id=category_id, name=category.name)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The category '{category.name}' already exists."
        )
    except Exception as e:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}"
        )
    finally:
        conn.close()

@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate):
    # Establish a database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    # Execute SQL query to update the category name
    cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (category.name, category_id))
    if cursor.rowcount == 0:
        # Handle case where the category ID does not exist
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")
    conn.commit()
    conn.close()
    return Category(id=category_id, name=category.name)

@router.delete("/categories/{category_id}", response_model=dict)
def delete_category(category_id: int):
    # Establish a database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    # Execute SQL query to delete the category
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    if cursor.rowcount == 0:
        # Handle case where the category ID does not exist
        conn.close()
        raise HTTPException(status_code=404, detail="Category not found")
    conn.commit()
    conn.close()
    return {"detail": "Category deleted"}