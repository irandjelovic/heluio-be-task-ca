from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class Item:
    id: Optional[UUID] = None
    name: str = None
    description: str = None
    price: float = None
    quantity: int = None
