import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from be_task_ca.database import Base
from be_task_ca.item.service import item_foreign_key
from be_task_ca.user.entities import CartItem, User


class CartItemDB(Base):
    __tablename__ = "cart_items"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(item_foreign_key()), primary_key=True
    )
    quantity: Mapped[int]

    def to_entity(self) -> CartItem:
        return CartItem(
            user_id=self.user_id, item_id=self.item_id, quantity=self.quantity
        )

    @staticmethod
    def from_entity(db_cart_item: CartItem) -> "CartItemDB":
        return CartItemDB(
            user_id=db_cart_item.user_id,
            item_id=db_cart_item.item_id,
            quantity=db_cart_item.quantity,
        )


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4(),
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    shipping_address: Mapped[str] = mapped_column(default=None)
    cart_items: Mapped[List["CartItemDB"]] = relationship()

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=self.hashed_password,
            shipping_address=self.shipping_address,
            cart_items=[ci.to_entity() for ci in self.cart_items],
        )

    @staticmethod
    def from_entity(db_user: User) -> "UserDB":
        return UserDB(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            hashed_password=db_user.hashed_password,
            shipping_address=db_user.shipping_address,
            cart_items=[CartItemDB.from_entity(ci) for ci in db_user.cart_items or []],
        )
