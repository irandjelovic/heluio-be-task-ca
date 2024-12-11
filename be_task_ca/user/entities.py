from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class CartItem:
    user_id: UUID = None
    item_id: UUID = None
    quantity: int = None


@dataclass
class User:
    id: UUID = None
    email: str = None
    first_name: str = None
    last_name: str = None
    hashed_password: str = None
    shipping_address: str = None
    cart_items: List[CartItem] = None
