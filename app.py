import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Base URL for API
API_BASE_URL = os.getenv("API_BASE_URL")


# Helper functions
def get_categories():
    """
    Fetches the list of categories from the API.

    Returns:
        list: A list of categories retrieved from the API.
    """
    response = requests.get(f"{API_BASE_URL}/categories/")
    return response.json()


def get_recipes(cuisine=None, difficulty=None):
    """
    Fetches the list of recipes from the API with optional filtering by cuisine and difficulty.

    Returns:
        list: A list of recipes retrieved from the API, possibly filtered by the provided parameters.
    """
    params = {}
    if cuisine:
        params['cuisine'] = cuisine
    if difficulty:
        params['difficulty'] = difficulty
    response = requests.get(f"{API_BASE_URL}/recipes/", params=params)
    return response.json()


def create_category(category_name):
    """
    Sends a request to create a new category.

    Returns:
        dict: The response from the API, typically containing the details of the created category.
    """
    response = requests.post(f"{API_BASE_URL}/categories/", json={"name": category_name})
    return response.json()


def update_category(category_id, new_name):
    """
    Sends a request to update an existing category.

    Returns:
        dict: The response from the API, typically containing the updated category details.
    """
    response = requests.put(f"{API_BASE_URL}/categories/{category_id}", json={"name": new_name})
    return response.json()


def delete_category(category_id):
    """
    Sends a request to delete an existing category.

    Returns:
        dict: The response from the API confirming the deletion of the category.
    """
    response = requests.delete(f"{API_BASE_URL}/categories/{category_id}")
    return response.json()


def create_recipe(recipe_name, description, ingredients, instructions, cuisine, difficulty, category_id):
    """
    Sends a request to create a new recipe.

    Returns:
        dict: The response from the API, typically containing the details of the created recipe.
    """
    response = requests.post(f"{API_BASE_URL}/recipes/", json={
        "name": recipe_name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cuisine": cuisine,
        "difficulty": difficulty,
        "category_id": category_id
    })
    return response.json()


def update_recipe(recipe_id, recipe_name, description, ingredients, instructions, cuisine, difficulty, category_id):
    """
    Sends a request to update an existing recipe.

    Returns:
        dict: The response from the API, typically containing the updated recipe details.
    """
    response = requests.put(f"{API_BASE_URL}/recipes/{recipe_id}", json={
        "name": recipe_name,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "cuisine": cuisine,
        "difficulty": difficulty,
        "category_id": category_id
    })
    return response.json()


def delete_recipe(recipe_id):
    """
    Sends a request to delete an existing recipe.

    Returns:
        dict: The response from the API confirming the deletion of the recipe.
    """
    response = requests.delete(f"{API_BASE_URL}/recipes/{recipe_id}")
    return response.json()


# Streamlit App
st.title("Online Recipe Book")

# Sidebar Navigation
menu = ["Dashboard", "Manage Recipes", "Manage Categories"]
selected_menu = st.sidebar.selectbox("Menu", menu)

if selected_menu == "Dashboard":
    st.header("Dashboard")

    # Display Recipes
    st.subheader("Recipes")
    recipe_list = get_recipes()
    if recipe_list:
        df_recipes = pd.DataFrame(recipe_list)
        # Remove 'id' column and add row numbers starting from 1
        if 'id' in df_recipes.columns:
            df_recipes = df_recipes.drop(columns=['id'])
        df_recipes.reset_index(drop=True, inplace=True)
        df_recipes.index += 1
        st.dataframe(df_recipes, use_container_width=True)
    else:
        st.info("No recipes found.")

    # Display Categories
    st.subheader("Categories")
    category_list = get_categories()
    if category_list:
        df_categories = pd.DataFrame(category_list)
        # Remove 'id' column and add row numbers starting from 1
        if 'id' in df_categories.columns:
            df_categories = df_categories.drop(columns=['id'])
        df_categories.reset_index(drop=True, inplace=True)
        df_categories.index += 1
        st.dataframe(df_categories, use_container_width=True)
    else:
        st.info("No categories found.")

elif selected_menu == "Manage Recipes":
    st.header("Manage Recipes")

    st.subheader("Add a New Recipe")
    recipe_name = st.text_input("Recipe Name", key="new_recipe_name")
    recipe_description = st.text_area("Description", key="new_recipe_description")
    recipe_ingredients = st.text_area("Ingredients", key="new_recipe_ingredients")
    recipe_instructions = st.text_area("Instructions", key="new_recipe_instructions")
    recipe_cuisine = st.text_input("Cuisine", key="new_recipe_cuisine")
    recipe_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="new_recipe_difficulty")

    category_list = get_categories()
    if category_list:
        category_names = [cat['name'] for cat in category_list]
        selected_category_name = st.selectbox("Category", category_names, key="new_recipe_category")
        selected_category_id = next(cat['id'] for cat in category_list if cat['name'] == selected_category_name)
    else:
        st.error("Failed to retrieve categories.")
        selected_category_id = None

    if st.button("Add Recipe", key="add_recipe_button"):
        if all([recipe_name, recipe_ingredients, recipe_instructions, recipe_cuisine, recipe_difficulty, selected_category_id is not None]):
            create_recipe(recipe_name, recipe_description, recipe_ingredients, recipe_instructions, recipe_cuisine, recipe_difficulty, selected_category_id)
            st.success(f"Recipe '{recipe_name}' added successfully!")
        else:
            st.error("All fields must be filled and category selected to add a recipe.")

    # Manage Recipe Edit and Delete
    st.subheader("Edit or Delete Recipe")
    recipe_list = get_recipes()
    if recipe_list:
        recipe_names = [recipe['name'] for recipe in recipe_list]
        manage_action = st.radio("Choose action", ["Edit", "Delete"], key="manage_recipe_action")

        if manage_action == "Edit":
            recipe_to_edit = st.selectbox("Select a recipe to edit", recipe_names, key="edit_recipe_select")
            if recipe_to_edit:
                selected_recipe = next(recipe for recipe in recipe_list if recipe['name'] == recipe_to_edit)
                st.subheader(f"Edit Recipe: {selected_recipe['name']}")
                edit_name = st.text_input("Recipe Name", value=selected_recipe['name'], key="edit_recipe_name")
                edit_description = st.text_area("Description", value=selected_recipe['description'], key="edit_recipe_description")
                edit_ingredients = st.text_area("Ingredients", value=selected_recipe['ingredients'], key="edit_recipe_ingredients")
                edit_instructions = st.text_area("Instructions", value=selected_recipe['instructions'], key="edit_recipe_instructions")
                edit_cuisine = st.text_input("Cuisine", value=selected_recipe['cuisine'], key="edit_recipe_cuisine")
                edit_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=["Easy", "Medium", "Hard"].index(selected_recipe['difficulty']), key="edit_recipe_difficulty")

                category_list = get_categories()
                if category_list:
                    category_names = [cat['name'] for cat in category_list]
                    edit_category_name = st.selectbox("Category", category_names, index=category_names.index(next(cat['name'] for cat in category_list if cat['id'] == selected_recipe['category_id'])), key="edit_recipe_category")
                    edit_category_id = next(cat['id'] for cat in category_list if cat['name'] == edit_category_name)
                else:
                    st.error("Failed to retrieve categories.")
                    edit_category_id = None

                if st.button("Update Recipe", key="update_recipe_button"):
                    if all([edit_name, edit_ingredients, edit_instructions, edit_cuisine, edit_difficulty, edit_category_id is not None]):
                        update_recipe(selected_recipe['id'], edit_name, edit_description, edit_ingredients, edit_instructions, edit_cuisine, edit_difficulty, edit_category_id)
                        st.success(f"Recipe '{edit_name}' updated successfully!")
                    else:
                        st.error("All fields must be filled and category selected to update a recipe.")

        elif manage_action == "Delete":
            recipe_to_delete = st.selectbox("Select a recipe to delete", recipe_names, key="delete_recipe_select")
            if recipe_to_delete:
                selected_recipe = next(recipe for recipe in recipe_list if recipe['name'] == recipe_to_delete)
                if st.button(f"Delete {selected_recipe['name']}", key="delete_recipe_button"):
                    delete_recipe(selected_recipe['id'])
                    st.success(f"Recipe '{selected_recipe['name']}' deleted successfully!")
    else:
        st.info("No recipes available to manage.")

elif selected_menu == "Manage Categories":
    st.header("Manage Categories")

    st.subheader("Add a New Category")
    new_category_name = st.text_input("New Category Name", key="new_category_name")
    if st.button("Add Category", key="add_category_button"):
        if new_category_name:
            create_category(new_category_name)
            st.success(f"Category '{new_category_name}' added successfully!")
        else:
            st.error("Category name cannot be empty.")

    # Manage Category Edit and Delete
    st.subheader("Edit or Delete Category")
    category_list = get_categories()
    if category_list:
        category_names = [category['name'] for category in category_list]
        manage_action = st.radio("Choose action", ["Edit", "Delete"], key="manage_category_action")

        if manage_action == "Edit":
            category_to_edit = st.selectbox("Select a category to edit", category_names, key="edit_category_select")
            if category_to_edit:
                selected_category = next(category for category in category_list if category['name'] == category_to_edit)
                st.subheader(f"Edit Category: {selected_category['name']}")
                new_category_name = st.text_input("Category Name", value=selected_category['name'], key="edit_category_name")
                if st.button("Update Category", key="update_category_button"):
                    if new_category_name:
                        update_category(selected_category['id'], new_category_name)
                        st.success(f"Category '{new_category_name}' updated successfully!")
                    else:
                        st.error("Category name cannot be empty.")

        elif manage_action == "Delete":
            category_to_delete = st.selectbox("Select a category to delete", category_names, key="delete_category_select")
            if category_to_delete:
                selected_category = next(category for category in category_list if category['name'] == category_to_delete)
                if st.button(f"Delete {selected_category['name']}", key="delete_category_button"):
                    delete_category(selected_category['id'])
                    st.success(f"Category '{selected_category['name']}' deleted successfully!")
    else:
        st.info("No categories available to manage.")