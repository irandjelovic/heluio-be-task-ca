from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from .entities import Item
from ..database import Base


class ItemDB(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4(),
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]

    def to_entity(self) -> Item:
        return Item(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
        )

    @staticmethod
    def from_entity(item: Item) -> "ItemDB":
        return ItemDB(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
