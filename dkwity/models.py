from pydantic import BaseModel
from typing import Optional

class Clients(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: Optional[bool] = None

class Carts(BaseModel):
    id: Optional[int] = None
    client_id: int
    items: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    became_order: Optional[bool] = None
    became_order_at: Optional[str] = None

class Orders(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    cart_id: int
    items: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_shipped: Optional[bool] = None
    shipped_at: Optional[str] = None
    total_price: Optional[float] = None
    item_qty: Optional[int] = None

class Items(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: Optional[bool] = None