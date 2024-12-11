from typing import List
from uuid import UUID

from .exceptions import (
    UserEmailDuplicateError,
    UserNotExistsError,
    ItemsNotEnoughError,
    ItemAlreadyAdded,
    ItemNotExistsError,
)
from .model import CartItem, User
from .repository.repository import Repository
from ..item.service import Item, find_item_by_id


def create_user(user: User, repo: Repository) -> User:
    existing_user: User = repo.find_user_by_email(user.email)
    if existing_user is not None:
        raise UserEmailDuplicateError(
            f"An user with this email adress already exists: {user.email}"
        )

    return repo.save_user(user)


def add_item_to_cart(user_id: UUID, cart_item: CartItem, repo: Repository) -> CartItem:
    user: User = repo.find_user_by_id(user_id)
    if user is None:
        raise UserNotExistsError("User does not exist")

    existing_item: Item = find_item_by_id(cart_item.item_id)
    if existing_item is None:
        raise ItemNotExistsError("Item does not exist")
    if existing_item.quantity < cart_item.quantity:
        raise ItemsNotEnoughError(
            f"Not enough items in stock: requested={cart_item.quantity}, stock={existing_item.quantity}"
        )

    item_ids = [o.item_id for o in user.cart_items or []]
    if existing_item.id in item_ids:
        raise ItemAlreadyAdded("Item already in cart")

    new_cart_item: CartItem = CartItem(
        user_id=user.id, item_id=existing_item.id, quantity=cart_item.quantity
    )

    if user.cart_items is None:
        user.cart_items = []
    user.cart_items.append(new_cart_item)
    repo.save_user(user)

    return new_cart_item


def list_items_in_cart(user_id, repo) -> List[CartItem]:
    return repo.find_cart_items_for_user_id(user_id)
