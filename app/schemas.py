from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    name : str
    email : str
    created_at : datetime
    role : str

    class Config:
        from_attributes = True

class Category(BaseModel):
    name : str

class CategoryResponse(BaseModel):
    id : int
    name : str
    
    class Config:
        from_attributes = True

class Product(BaseModel):
    name : str
    description :str
    price : int
    stock_quantity : int
    category_id : int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(BaseModel):
    id : int
    name : str
    description : str
    price : int
    stock_quantity : int
    category_id : int
    is_active : bool
    created_at : datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id : int
    total_amount: int
    status: str


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    total_amount: Optional[int] = None
    status: Optional[str] = None


class OrderResponse(BaseModel):
    id : int
    user_id : int
    total_amount: int
    status: str
    created_at: datetime

    class Config:
        from_attributes=True

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: int

class OrderItemUpdate(BaseModel):
    order_id:Optional[int] = None
    product_id:Optional[int] = None
    quantity:Optional[int] = None
    price_at_purchase:Optional[int] = None

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: int

    class Config:
        from_attributes = True

class CartBase(BaseModel):
    user_id : int

class CartResponse(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True
    
class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    cart_id:Optional[int] = None
    product_id:Optional[int] = None
    quantity:Optional[int] = None

class CartItemResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True