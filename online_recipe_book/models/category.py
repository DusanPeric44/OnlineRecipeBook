from pydantic import BaseModel

# za kategoriju koja sadrzi samo name
class CategoryBase(BaseModel):
    name: str

# Za kreiranje unutar baze
class CategoryCreate(CategoryBase):
    pass

# Iz baze podataka
class CategoryResponse(BaseModel):
    id: str
    name: str

class Category(CategoryBase):
    id: int