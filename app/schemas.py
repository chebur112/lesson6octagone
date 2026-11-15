from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    
    
class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    
    
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    price: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    url: str = ""
    category_id: int
    

class BookCreate(BookBase):
    pass


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int    
